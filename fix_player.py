import re

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

# Replace definition
old_def = """@OptIn(androidx.media3.common.util.UnstableApi::class, androidx.compose.material3.ExperimentalMaterial3Api::class)
@Composable
@Suppress("OPT_IN_USAGE")
fun PlayerScreen(videoUrl: String, title: String, onBack: () -> Unit) {"""
new_def = """@OptIn(androidx.media3.common.util.UnstableApi::class, androidx.compose.material3.ExperimentalMaterial3Api::class)
@Composable
@Suppress("OPT_IN_USAGE")
fun PlayerScreen(mediaId: String, isMovie: Boolean, title: String, onBack: () -> Unit, viewModel: PlayerViewModel = androidx.lifecycle.viewmodel.compose.viewModel()) {
    val uiState by viewModel.uiState.collectAsState()
    
    LaunchedEffect(mediaId) {
        viewModel.initialize(mediaId, isMovie, title)
    }
"""
content = content.replace(old_def, new_def)


# We need to change ExoPlayer initialization to react to currentVideoUrl from viewModel
old_exo = """    val exoPlayer = remember {
        ExoPlayer.Builder(context).build().apply {
            val mediaItem = MediaItem.fromUri(videoUrl)
            setMediaItem(mediaItem)
            prepare()
            playWhenReady = true
            addListener(object : Player.Listener {
                override fun onIsPlayingChanged(isPlayingChanged: Boolean) {
                    isPlaying = isPlayingChanged
                }
                override fun onPlaybackStateChanged(state: Int) {
                    if (state == Player.STATE_READY) {
                        totalDuration = duration.coerceAtLeast(0L)
                    }
                }
            })
        }
    }"""
new_exo = """    val exoPlayer = remember {
        ExoPlayer.Builder(context).build().apply {
            addListener(object : Player.Listener {
                override fun onIsPlayingChanged(isPlayingChanged: Boolean) {
                    isPlaying = isPlayingChanged
                }
                override fun onPlaybackStateChanged(state: Int) {
                    if (state == Player.STATE_READY) {
                        totalDuration = duration.coerceAtLeast(0L)
                    }
                }
            })
        }
    }
    
    LaunchedEffect(uiState.currentVideoUrl) {
        uiState.currentVideoUrl?.let { url ->
            val mediaItem = MediaItem.fromUri(url)
            exoPlayer.setMediaItem(mediaItem)
            exoPlayer.prepare()
            exoPlayer.playWhenReady = true
        }
    }"""
content = content.replace(old_exo, new_exo)

# Replace the state variables that are now in ViewModel
old_state = """    // Server & Website state
    var showServerSheet by remember { mutableStateOf(false) }
    var showWebsiteSheet by remember { mutableStateOf(false) }
    var currentServer by remember { mutableStateOf("Server 1") }
    var currentWebsite by remember { mutableStateOf("VidSrc") }"""
new_state = """    // Server & Website state
    var showServerSheet by remember { mutableStateOf(false) }
    var showWebsiteSheet by remember { mutableStateOf(false) }"""
content = content.replace(old_state, new_state)

# Add HiddenVideoExtractor next to AndroidView
old_android_view = """        AndroidView(
            factory = { ctx ->
                PlayerView(ctx).apply {
                    player = exoPlayer
                    useController = false
                }
            },
            modifier = Modifier.fillMaxSize()
        )"""
new_android_view = """        AndroidView(
            factory = { ctx ->
                PlayerView(ctx).apply {
                    player = exoPlayer
                    useController = false
                }
            },
            modifier = Modifier.fillMaxSize()
        )
        
        uiState.extractionUrl?.let { url ->
            HiddenVideoExtractor(
                url = url,
                onVideoUrlFound = { extractedUrl ->
                    viewModel.setExtractedUrl(extractedUrl)
                }
            )
        }
        
        if (uiState.isLoading) {
            Box(modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = 0.5f)), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    CircularProgressIndicator(color = Color(0xFFE50914))
                    Spacer(modifier = Modifier.height(16.dp))
                    Text("Connecting to ${uiState.currentWebsite} / ${uiState.currentServer}...", color = Color.White)
                }
            }
        }"""
content = content.replace(old_android_view, new_android_view)

# In TopBar, update title and current website text
content = content.replace('Text("Now Playing"', 'Text(if(uiState.isMovie) "Movie" else "Series",')
content = content.replace('Text("Episode 1"', 'Text(uiState.title')
content = content.replace('Text("WEBSITE", color = Color.Gray', 'Text(uiState.currentWebsite.uppercase(), color = Color.Gray')
content = content.replace('Text("SERVER", color = Color.Gray', 'Text(uiState.currentServer.uppercase(), color = Color.Gray')
content = content.replace('QualityAction(currentQuality', 'QualityAction(uiState.currentQuality')

# Hide Episodes button if isMovie
content = content.replace('BottomAction(icon = Icons.Default.VideoLibrary, text = "Episodes") { showEpisodesSheet = true }', 'if (!uiState.isMovie) { BottomAction(icon = Icons.Default.VideoLibrary, text = "Episodes") { showEpisodesSheet = true } }')

# Replace EpisodesSheet Content
old_episodes = """                Column {
                    repeat(5) { i ->
                        val epNum = i + 1
                        TextButton(
                            onClick = { showEpisodesSheet = false },
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Text("Episode $epNum", color = Color.White)
                        }
                    }
                }"""
new_episodes = """                LazyColumn {
                    items(uiState.episodes) { ep ->
                        TextButton(
                            onClick = { 
                                viewModel.selectEpisode(ep)
                                showEpisodesSheet = false 
                            },
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Text(
                                "Episode ${ep.episodeNumber}: ${ep.title}", 
                                color = if (ep.id == uiState.currentEpisodeId) Color(0xFFE50914) else Color.White
                            )
                        }
                    }
                }"""
content = content.replace(old_episodes, new_episodes)


# Replace Websites Sheet Content
old_websites = """                val websites = listOf("VidSrc", "SuperStream", "FlixHQ", "Goku")
                websites.forEach { w ->
                    TextButton(
                        onClick = { 
                            currentWebsite = w
                            showWebsiteSheet = false
                            android.widget.Toast.makeText(context, "Switched source to $w", android.widget.Toast.LENGTH_SHORT).show()
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(w, color = if (w == currentWebsite) Color(0xFFE50914) else Color.White)
                    }
                }"""
new_websites = """                uiState.availableWebsites.forEach { w ->
                    TextButton(
                        onClick = { 
                            viewModel.selectWebsite(w)
                            showWebsiteSheet = false
                            android.widget.Toast.makeText(context, "Switched source to $w", android.widget.Toast.LENGTH_SHORT).show()
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(w, color = if (w == uiState.currentWebsite) Color(0xFFE50914) else Color.White)
                    }
                }"""
content = content.replace(old_websites, new_websites)


# Replace Servers Sheet Content
old_servers = """                val servers = listOf("Server 1", "Server 2", "VIP Server", "Fast Server")
                servers.forEach { s ->
                    TextButton(
                        onClick = { 
                            currentServer = s
                            showServerSheet = false
                            android.widget.Toast.makeText(context, "Switched to $s", android.widget.Toast.LENGTH_SHORT).show()
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(s, color = if (s == currentServer) Color(0xFFE50914) else Color.White)
                    }
                }"""
new_servers = """                uiState.availableServers.forEach { s ->
                    TextButton(
                        onClick = { 
                            viewModel.selectServer(s)
                            showServerSheet = false
                            android.widget.Toast.makeText(context, "Switched to $s", android.widget.Toast.LENGTH_SHORT).show()
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(s, color = if (s == uiState.currentServer) Color(0xFFE50914) else Color.White)
                    }
                }"""
content = content.replace(old_servers, new_servers)


with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)
