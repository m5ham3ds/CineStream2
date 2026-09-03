package com.example.ui.screens.details
import com.example.utils.SiteVerificationManager
import androidx.compose.ui.res.stringResource
import com.example.R

import android.content.Intent
import android.net.Uri
import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*

import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.material3.pulltorefresh.rememberPullToRefreshState

import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import coil.compose.AsyncImage
import com.example.data.model.DownloadItem
import com.example.data.model.LibraryItem
import com.example.data.repository.DownloadRepository
import com.example.data.repository.LibraryRepository
import com.example.domain.models.CastMember
import com.example.domain.models.Episode
import com.example.domain.models.Season
import com.example.domain.models.VideoTrailer
import com.example.ui.components.SourceSelectionSheet
import com.example.ui.ViewModelFactory
import kotlinx.coroutines.launch
import java.net.URLEncoder

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MovieDetailsScreen(
    onPersonClick: (String) -> Unit = {},
    movieId: String, 
    onBack: () -> Unit,
    onPlay: (String, String) -> Unit,
    viewModel: MovieDetailsViewModel = viewModel(factory = ViewModelFactory())
) {
    val uiState by viewModel.uiState.collectAsState()
    val context = LocalContext.current
    val downloadRepository = remember { DownloadRepository(context) }
    val libraryRepository = remember { LibraryRepository(context) }
    val scope = rememberCoroutineScope()
    val libraryItems by libraryRepository.getLibraryItems().collectAsState(initial = emptyList())
    val downloadItems by downloadRepository.getDownloadItems().collectAsState(initial = emptyList())
    
    val isFavorite = libraryItems.any { it.id == movieId }
    val downloadItem = downloadItems.find { it.id == movieId }
    var showDeleteConfirm by remember { mutableStateOf(false) }

    LaunchedEffect(movieId) {
        viewModel.loadMovie(movieId)
    }

    Scaffold(
        containerColor = MaterialTheme.colorScheme.background
    ) { padding ->
        if (uiState.isLoading) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { CircularProgressIndicator() }
        } else if (uiState.movie != null) {
            val movie = uiState.movie!!
            val ctx = LocalContext.current
            val historyRepository = remember { com.example.data.repository.HistoryRepository(ctx) }
            var showSourceSheet by remember { mutableStateOf(false) }
            var isDownloadMode by remember { mutableStateOf(false) }
            var selectedTrailerId by remember { mutableStateOf<String?>(null) }

            val ptrState = rememberPullToRefreshState()
            PullToRefreshBox(
                isRefreshing = uiState.isLoading,
                onRefresh = { viewModel.loadMovie(movieId) },
                state = ptrState,
                modifier = Modifier.fillMaxSize().padding(bottom = padding.calculateBottomPadding())
            ) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
            ) {
                
                if (showDeleteConfirm) {
                    AlertDialog(
                        onDismissRequest = { showDeleteConfirm = false },
                        title = { Text(stringResource(R.string.delete_download), color = MaterialTheme.colorScheme.onBackground) },
                        text = { Text(stringResource(R.string.delete_download_confirm), color = MaterialTheme.colorScheme.onSurfaceVariant) },
                        confirmButton = {
                            TextButton(onClick = {
                                downloadItem?.let {
                                    scope.launch { downloadRepository.removeFromDownloads(it) }
                                }
                                showDeleteConfirm = false
                            }) { Text(stringResource(R.string.yes_delete), color = Color.Red) }
                        },
                        dismissButton = {
                            TextButton(onClick = { showDeleteConfirm = false }) { Text(stringResource(R.string.cancel), color = MaterialTheme.colorScheme.onBackground) }
                        },
                        containerColor = MaterialTheme.colorScheme.surface
                    )
                }
                
                // Hero Image or Video Player

                if (selectedTrailerId != null) {
                    Box(modifier = Modifier.fillMaxWidth().aspectRatio(16f/9f)) {
                        com.example.ui.components.InlineYouTubePlayer(
                            videoId = selectedTrailerId!!,
                            modifier = Modifier.fillMaxSize()
                        )
                    }
                    Spacer(modifier = Modifier.height(16.dp))
                    Column(modifier = Modifier.padding(horizontal = 16.dp)) {
                        Text(text = movie.title, style = MaterialTheme.typography.displaySmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)
                        Spacer(modifier = Modifier.height(8.dp))
                        
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text("${movie.year} • ${movie.genres.take(3).joinToString(" • ")}", color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodyMedium)
                        }
                        Spacer(modifier = Modifier.height(8.dp))
                        
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Default.Star, contentDescription = "Rating", tint = Color(0xFFFFC107), modifier = Modifier.size(18.dp))
                                Spacer(modifier = Modifier.width(4.dp))
                                Text(String.format("%.1f", movie.rating), color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
                            }
                            Badge(containerColor = Color.DarkGray) { Text("18+", color = MaterialTheme.colorScheme.onBackground) }
                        }
                    }
                } else {
                    Box(modifier = Modifier.fillMaxWidth().aspectRatio(0.8f)) {
                        AsyncImage(
                            model = movie.posterUrl.takeIf { it.isNotBlank() } ?: movie.backdropUrl,
                            contentDescription = movie.title,
                            contentScale = ContentScale.Crop,
                            modifier = Modifier.fillMaxSize()
                        )
                        Box(modifier = Modifier.fillMaxSize().background(
                            Brush.verticalGradient(
                                colors = listOf(Color.Transparent, Color.Black.copy(alpha=0.6f), MaterialTheme.colorScheme.background),
                                startY = 0f
                            )
                        ))
                        Column(
                            modifier = Modifier.align(Alignment.BottomStart).padding(16.dp)
                        ) {
                            Text(text = movie.title, style = MaterialTheme.typography.displaySmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)
                            Spacer(modifier = Modifier.height(8.dp))
                            
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text("${movie.year} • ${movie.genres.take(3).joinToString(" • ")}", color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodyMedium)
                            }
                            Spacer(modifier = Modifier.height(8.dp))
                            
                            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Default.Star, contentDescription = "Rating", tint = Color(0xFFFFC107), modifier = Modifier.size(18.dp))
                                    Spacer(modifier = Modifier.width(4.dp))
                                    Text(String.format("%.1f", movie.rating), color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
                                }
                                Badge(containerColor = Color.DarkGray) { Text("18+", color = MaterialTheme.colorScheme.onBackground) } // Placeholder for age rating
                            }
                        }
                    }
                }
                
                // Action Buttons
                Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(16.dp), verticalAlignment = Alignment.CenterVertically) {
                    Button(
                        onClick = { 
                            if (downloadItem?.isCompleted == true) {
                                onPlay(movie.title, "local_offline_file://${downloadItem.id}")
                            } else {
                                onPlay(movie.title, "") 
                            }
                        },
                        modifier = Modifier.weight(1f).height(50.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                    ) {
                        Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = MaterialTheme.colorScheme.onBackground)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(if (downloadItem?.isCompleted == true) "Resume Offline" else "Resume", color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
                    }
                    IconButton(
                        onClick = { 
                            if (downloadItem?.isCompleted == true) {
                                showDeleteConfirm = true
                            } else if (downloadItem == null) {
                                isDownloadMode = true
                                showSourceSheet = true
                            }
                        },
                        modifier = Modifier.size(50.dp).background(Color.DarkGray, CircleShape)
                    ) {
                        if (downloadItem?.isCompleted == true) {
                            Icon(Icons.Default.DownloadDone, contentDescription = "Downloaded", tint = Color.Green)
                        } else if (downloadItem != null) {
                            CircularProgressIndicator(progress = { downloadItem.progress }, color = MaterialTheme.colorScheme.primary, modifier = Modifier.size(24.dp))
                        } else {
                            Icon(Icons.Default.Download, contentDescription = "Download", tint = MaterialTheme.colorScheme.onBackground)
                        }
                    }
                    IconButton(
                        onClick = { 
                            scope.launch {
                                val item = LibraryItem(id = movie.id, title = movie.title, posterUrl = movie.posterUrl, isMovie = true)
                                if (isFavorite) libraryRepository.removeFromLibrary(item)
                                else libraryRepository.addToLibrary(item)
                            }
                        },
                        modifier = Modifier.size(50.dp).background(Color.DarkGray, CircleShape)
                    ) {
                        Icon(if (isFavorite) Icons.Default.Bookmark else Icons.Default.BookmarkBorder, contentDescription = "Favorite", tint = MaterialTheme.colorScheme.onBackground)
                    }
                }
                
                Spacer(modifier = Modifier.height(24.dp))
                
                // Trailers
                if (movie.trailers.isNotEmpty()) {
                    Text(stringResource(R.string.trailers), color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 16.dp))
                    Spacer(modifier = Modifier.height(8.dp))
                    LazyRow(contentPadding = PaddingValues(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        items(movie.trailers) { trailer ->
                            TrailerCard(trailer) {
                                selectedTrailerId = trailer.key
                            }
                        }
                    }
                    Spacer(modifier = Modifier.height(24.dp))
                }
                
                // Overview
                Text(stringResource(R.string.overview), color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 16.dp))
                Spacer(modifier = Modifier.height(8.dp))
                Text(movie.overview, color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodyMedium, modifier = Modifier.padding(horizontal = 16.dp))
                
                Spacer(modifier = Modifier.height(24.dp))
                
                // Cast
                if (movie.cast.isNotEmpty()) {
                    Text(stringResource(R.string.cast), color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 16.dp))
                    Spacer(modifier = Modifier.height(8.dp))
                    LazyRow(contentPadding = PaddingValues(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                        items(movie.cast) { CastMemberCard(it) { onPersonClick(it.id) } }
                    }
                    Spacer(modifier = Modifier.height(32.dp))
                }
            }

            }
            if (showSourceSheet) {
                SourceSelectionSheet(
                    mediaId = movie.id,
                    isMovie = true,
                    onDismiss = { showSourceSheet = false },
                    onSourceSelected = { source ->
                        showSourceSheet = false
                        if (isDownloadMode) {
                            scope.launch {
                                downloadRepository.addToDownloads(DownloadItem(
                                    id = movie.id, title = movie.title, posterUrl = movie.posterUrl, isMovie = true, quality = source.quality
                                ))
                                com.example.utils.AndroidDownloader.downloadVideo(ctx, source.url, "${movie.title} - ${source.quality}")
                            }
                        } else {
                            scope.launch {
                                historyRepository.addToHistory(
                                    com.example.data.model.HistoryItem(
                                        id = movie.id,
                                        title = movie.title,
                                        posterUrl = movie.posterUrl,
                                        isMovie = true
                                    )
                                )
                                onPlay(movie.title, source.url)
                            }
                        }
                    }
                )
            }

            IconButton(
                onClick = onBack,
                modifier = Modifier
                    .padding(top = padding.calculateTopPadding() + 8.dp, start = 16.dp)
                    .background(Color.Black.copy(alpha=0.3f), CircleShape)
            ) {
                Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = MaterialTheme.colorScheme.onBackground)
            }

        }
    }
}

@OptIn(ExperimentalMaterial3Api::class, androidx.compose.foundation.ExperimentalFoundationApi::class)
@Composable
fun SeriesDetailsScreen(
    onPersonClick: (String) -> Unit = {},
    seriesId: String,
    onBack: () -> Unit,
    onPlay: (String, String) -> Unit
) {
    val context = LocalContext.current
    val viewModel: SeriesDetailsViewModel = viewModel(factory = ViewModelFactory())
    val uiState by viewModel.uiState.collectAsState()
    val scope = rememberCoroutineScope()
    val libraryRepository = remember { LibraryRepository(context) }
    val isFavorite by libraryRepository.isItemInLibrary(seriesId).collectAsState(initial = false)
    val downloadRepository = remember { DownloadRepository(context) }
    val historyRepository = remember { com.example.data.repository.HistoryRepository(context) }
    val watchedRepo = remember { com.example.data.repository.WatchedEpisodeRepository(context) }
    val watchedEpisodes by watchedRepo.getAllWatched().collectAsState(initial = emptyList())
    val watchedEpisodeIds = watchedEpisodes.map { it.id }.toSet()

    var selectedEpisodeForSource by remember { mutableStateOf<Episode?>(null) }
    var isDownloadMode by remember { mutableStateOf(false) }
    var showBatchDownloadSheet by remember { mutableStateOf(false) }
    var selectedTrailerId by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(seriesId) {
        viewModel.loadSeries(seriesId)
    }

    val pullRefreshState = rememberPullToRefreshState()
    PullToRefreshBox(
        isRefreshing = uiState.isLoading,
        onRefresh = { viewModel.loadSeries(seriesId) },
        state = pullRefreshState
    ) {
        val series = uiState.series
        if (series == null && !uiState.isLoading) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text(uiState.error ?: "Failed to load details", color = MaterialTheme.colorScheme.error)
            }
            return@PullToRefreshBox
        }

        if (series != null) {
            val scrollState = rememberScrollState()
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .verticalScroll(scrollState)
            ) {
                if (selectedTrailerId != null) {
                    Box(modifier = Modifier.fillMaxWidth().aspectRatio(16f/9f)) {
                        com.example.ui.components.InlineYouTubePlayer(
                            videoId = selectedTrailerId!!,
                            modifier = Modifier.fillMaxSize()
                        )
                    }
                } else {
                    Box(modifier = Modifier.fillMaxWidth().height(400.dp)) {
                        AsyncImage(
                            model = series.posterUrl,
                            contentDescription = series.title,
                            contentScale = ContentScale.Crop,
                            modifier = Modifier.fillMaxSize()
                        )
                        Box(
                            modifier = Modifier
                                .fillMaxSize()
                                .background(
                                    Brush.verticalGradient(
                                        colors = listOf(Color.Transparent, MaterialTheme.colorScheme.background),
                                        startY = 300f
                                    )
                                )
                        )
                    }
                }

                Column(modifier = Modifier.padding(16.dp)) {
                    Text(series.title, style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)
                    Spacer(modifier = Modifier.height(8.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.Star, contentDescription = "Rating", tint = Color(0xFFFFC107), modifier = Modifier.size(20.dp))
                        Spacer(modifier = Modifier.width(4.dp))
                        Text(String.format("%.1f", series.rating), style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onBackground)
                        Spacer(modifier = Modifier.width(16.dp))
                        Text(series.year.toString(), style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    val firstUnplayedEpisode = uiState.episodes.firstOrNull { !watchedEpisodeIds.contains(it.id) } ?: uiState.episodes.firstOrNull()

                    // Action Buttons
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                        Button(
                            onClick = {
                                if (firstUnplayedEpisode != null) {
                                    selectedEpisodeForSource = firstUnplayedEpisode
                                    isDownloadMode = false
                                } else {
                                    Toast.makeText(context, "No episodes available", Toast.LENGTH_SHORT).show()
                                }
                            },
                            modifier = Modifier.weight(1f),
                            shape = RoundedCornerShape(8.dp)
                        ) {
                            Icon(Icons.Default.PlayArrow, contentDescription = "Play")
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(stringResource(R.string.play))
                        }
                        IconButton(
                            onClick = {
                                showBatchDownloadSheet = true
                            },
                            modifier = Modifier.background(MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(8.dp))
                        ) {
                            Icon(Icons.Default.Download, contentDescription = "Download")
                        }
                        IconButton(
                            onClick = {
                                scope.launch {
                                    if (isFavorite) {
                                        libraryRepository.removeFromLibrary(LibraryItem(id = series.id, title = series.title, posterUrl = series.posterUrl, isMovie = false))
                                    } else {
                                        libraryRepository.addToLibrary(
                                            LibraryItem(
                                                id = series.id,
                                                title = series.title,
                                                posterUrl = series.posterUrl,
                                                isMovie = false
                                            )
                                        )
                                    }
                                }
                            },
                            modifier = Modifier.background(MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(8.dp))
                        ) {
                            Icon(if (isFavorite) Icons.Default.Favorite else Icons.Default.FavoriteBorder, contentDescription = "Add to Favorites", tint = if (isFavorite) Color.Red else MaterialTheme.colorScheme.onBackground)
                        }
                    }

                    Spacer(modifier = Modifier.height(24.dp))
                    Text(series.overview, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onBackground)
                    Spacer(modifier = Modifier.height(24.dp))

                    if (series.trailers.isNotEmpty()) {
                        Text(stringResource(R.string.trailers), color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(8.dp))
                        LazyRow(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                            items(series.trailers) { trailer ->
                                TrailerCard(trailer) { selectedTrailerId = trailer.key }
                            }
                        }
                        Spacer(modifier = Modifier.height(32.dp))
                    }
                    if (series.cast.isNotEmpty()) {
                        Text(stringResource(R.string.cast), color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(8.dp))
                        LazyRow(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                            items(series.cast) { CastMemberCard(it) { onPersonClick(it.id) } }
                        }
                        Spacer(modifier = Modifier.height(32.dp))
                    }
                }

                // Seasons & Episodes
                if (series.seasons.isNotEmpty()) {
                    Text(stringResource(R.string.seasons_and_episodes), color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 16.dp))
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    // Season Tabs
                    LazyRow(contentPadding = PaddingValues(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        items(series.seasons.filter { it.seasonNumber > 0 }) { season ->
                            val isSelected = uiState.selectedSeason?.id == season.id
                            FilterChip(
                                selected = isSelected,
                                onClick = { viewModel.selectSeason(season) },
                                label = { Text(stringResource(R.string.season_number, season.seasonNumber)) },
                                colors = FilterChipDefaults.filterChipColors(
                                    selectedContainerColor = MaterialTheme.colorScheme.primary,
                                    selectedLabelColor = MaterialTheme.colorScheme.onBackground
                                )
                            )
                        }
                    }
                    Spacer(modifier = Modifier.height(16.dp))

                    // Episodes
                    if (uiState.isEpisodesLoading) {
                        Box(modifier = Modifier.fillMaxWidth().padding(32.dp), contentAlignment = Alignment.Center) { CircularProgressIndicator() }
                    } else {
                        uiState.episodes.forEach { episode ->
                            val isWatched = watchedEpisodeIds.contains(episode.id)
                            EpisodeCard(
                                episode = episode,
                                isWatched = isWatched,
                                onClick = {
                                    selectedEpisodeForSource = episode
                                    isDownloadMode = false
                                },
                                onLongClick = {
                                    scope.launch {
                                        if (isWatched) watchedRepo.markAsUnwatched(episode.id)
                                        else watchedRepo.markAsWatched(episode.id)
                                    }
                                },
                                onDownloadClick = {
                                    selectedEpisodeForSource = episode
                                    isDownloadMode = true
                                }
                            )
                        }
                    }
                    Spacer(modifier = Modifier.height(32.dp))
                }
            }
            
            if (selectedEpisodeForSource != null) {
                SourceSelectionSheet(
                    mediaId = series.id,
                    mediaTitle = "${series.title} S${uiState.selectedSeason?.seasonNumber}E${selectedEpisodeForSource?.episodeNumber}",
                    isMovie = false,
                    episodeId = selectedEpisodeForSource?.id,
                    onDismiss = { selectedEpisodeForSource = null },
                    onSourceSelected = { source ->
                        val ep = selectedEpisodeForSource!!
                        selectedEpisodeForSource = null
                        if (isDownloadMode) {
                            scope.launch {
                                val fullTitle = "${series.title} - S${uiState.selectedSeason?.seasonNumber}E${ep.episodeNumber}"
                                downloadRepository.addToDownloads(DownloadItem(
                                    id = ep.id, title = fullTitle, posterUrl = ep.thumbnailUrl, isMovie = false, quality = source.quality
                                ))
                                com.example.utils.AndroidDownloader.downloadVideo(context, source.url, "$fullTitle - ${source.quality}")
                            }
                        } else {
                            scope.launch {
                                historyRepository.addToHistory(
                                    com.example.data.model.HistoryItem(
                                        id = series.id,
                                        title = series.title,
                                        posterUrl = series.posterUrl,
                                        isMovie = false
                                    )
                                )
                                watchedRepo.markAsWatched(ep.id)
                                onPlay("${series.title} - ${ep.title}", source.url)
                            }
                        }
                    }
                )
            }
            
            if (showBatchDownloadSheet) {
                com.example.ui.components.BatchDownloadSheet(
                    series = series,
                    currentSeason = uiState.selectedSeason,
                    episodes = uiState.episodes,
                    onDismiss = { showBatchDownloadSheet = false }
                )
            }

            IconButton(
                onClick = onBack,
                modifier = Modifier
                    .padding(top = WindowInsets.statusBars.asPaddingValues().calculateTopPadding() + 8.dp, start = 16.dp)
                    .background(Color.Black.copy(alpha=0.3f), CircleShape)
            ) {
                Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
            }
        }
    }
}

@Composable
fun TrailerCard(trailer: VideoTrailer, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .width(200.dp)
            .aspectRatio(16f/9f)
            .clip(RoundedCornerShape(8.dp))
            .clickable { onClick() }
    ) {
        AsyncImage(
            model = "https://img.youtube.com/vi/${trailer.key}/hqdefault.jpg",
            contentDescription = trailer.name,
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )
        Box(modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha=0.3f)), contentAlignment = Alignment.Center) {
            Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = Color.White, modifier = Modifier.size(48.dp))
        }
        Text(
            text = trailer.name,
            color = Color.White,
            style = MaterialTheme.typography.labelSmall,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
            modifier = Modifier.align(Alignment.BottomStart).padding(8.dp)
        )
    }
}

@Composable
fun CastMemberCard(cast: CastMember, onClick: () -> Unit) {
    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.width(80.dp).clickable { onClick() }) {
        AsyncImage(
            model = cast.profileUrl ?: "https://via.placeholder.com/150",
            contentDescription = cast.name,
            contentScale = ContentScale.Crop,
            modifier = Modifier.size(72.dp).clip(CircleShape).background(Color.DarkGray)
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(cast.name, color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.labelMedium, maxLines = 1, overflow = TextOverflow.Ellipsis)
        Text(cast.character, color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.labelSmall, maxLines = 1, overflow = TextOverflow.Ellipsis)
    }
}

@OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)
@Composable
fun EpisodeCard(
    episode: Episode,
    isWatched: Boolean,
    onClick: () -> Unit,
    onLongClick: () -> Unit,
    onDownloadClick: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .combinedClickable(
                onClick = onClick,
                onLongClick = onLongClick
            )
            .padding(horizontal = 16.dp, vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier.width(120.dp).aspectRatio(16f/9f).clip(RoundedCornerShape(8.dp))
        ) {
            AsyncImage(
                model = episode.thumbnailUrl,
                contentDescription = episode.title,
                contentScale = ContentScale.Crop,
                modifier = Modifier.fillMaxSize().background(Color.DarkGray)
            )
            Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = Color.White, modifier = Modifier.align(Alignment.Center))
        }
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = "${episode.episodeNumber}. ${episode.title}",
                color = if (isWatched) MaterialTheme.colorScheme.onBackground.copy(alpha = 0.5f) else MaterialTheme.colorScheme.onBackground,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Spacer(modifier = Modifier.height(4.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.Star, contentDescription = "Rating", tint = Color(0xFFFFC107), modifier = Modifier.size(12.dp))
                Spacer(modifier = Modifier.width(4.dp))
                Text(String.format("%.1f", episode.rating), color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.labelSmall)
                Spacer(modifier = Modifier.width(8.dp))
                Text("${episode.duration}m", color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.labelSmall)
            }
            Spacer(modifier = Modifier.height(4.dp))
            Text(episode.overview, color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodySmall, maxLines = 2, overflow = TextOverflow.Ellipsis)
        }
        IconButton(onClick = onDownloadClick) {
            Icon(Icons.Default.Download, contentDescription = "Download", tint = MaterialTheme.colorScheme.onBackground)
        }
    }
}
