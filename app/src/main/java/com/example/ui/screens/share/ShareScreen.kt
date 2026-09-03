package com.example.ui.screens.share

import android.Manifest
import android.os.Build
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.outlined.Folder
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material.icons.outlined.Movie
import androidx.compose.material.icons.outlined.QrCode2
import androidx.compose.material.icons.outlined.Shield
import androidx.compose.material.icons.outlined.Tv
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.model.DownloadItem
import com.example.data.repository.DownloadRepository
import com.example.utils.Endpoint
import com.example.utils.P2PManager
import com.example.utils.P2PState
import com.google.accompanist.permissions.ExperimentalPermissionsApi
import com.google.accompanist.permissions.rememberMultiplePermissionsState
import kotlinx.coroutines.launch
import java.io.File
import androidx.compose.foundation.lazy.LazyRow

@OptIn(ExperimentalPermissionsApi::class, ExperimentalMaterial3Api::class)
@Composable
fun ShareScreen(
    onBack: () -> Unit
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val p2pManager = remember { P2PManager(context) }
    val downloadRepository = remember { com.example.data.repository.DownloadRepository(context) }
    
    val p2pState by p2pManager.p2pState.collectAsState()
    val connectedEndpoint by p2pManager.connectedEndpoint.collectAsState()
    val discoveredEndpoints by p2pManager.discoveredEndpoints.collectAsState()
    val transferProgress by p2pManager.transferProgress.collectAsState()
    
    val allDownloads by downloadRepository.getDownloadItems().collectAsState(initial = emptyList())
    val completedDownloads = remember(allDownloads) { allDownloads.filter { it.isCompleted } }

    DisposableEffect(Unit) {
        p2pManager.onMovieReceived = { id, title, isMovie, posterUrl ->
            scope.launch {
                downloadRepository.addCompletedDownload(
                    DownloadItem(
                        id = id,
                        title = title,
                        posterUrl = posterUrl,
                        isMovie = isMovie,
                        quality = "1080p", // Inherited default
                        progress = 1f,
                        isCompleted = true
                    )
                )
            }
        }
        onDispose { p2pManager.stopAll() }
    }

    val permissions = if (Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.S) {
        listOf(
            Manifest.permission.BLUETOOTH_SCAN,
            Manifest.permission.BLUETOOTH_ADVERTISE,
            Manifest.permission.BLUETOOTH_CONNECT,
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.NEARBY_WIFI_DEVICES
        )
    } else {
        listOf(
            Manifest.permission.BLUETOOTH,
            Manifest.permission.BLUETOOTH_ADMIN,
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION
        )
    }
    
    val permissionsState = rememberMultiplePermissionsState(permissions)
    var showSendDialog by remember { mutableStateOf(false) }
    var showReceiveDialog by remember { mutableStateOf(false) }
    var pendingAction by remember { mutableStateOf<(() -> Unit)?>(null) }
    
    // Check permission logic
    val checkPermissionsAndRun = { action: () -> Unit ->
        if (permissionsState.allPermissionsGranted) {
            action()
        } else {
            pendingAction = action
            permissionsState.launchMultiplePermissionRequest()
        }
    }
    
    LaunchedEffect(permissionsState.allPermissionsGranted) {
        if (permissionsState.allPermissionsGranted && pendingAction != null) {
            pendingAction?.invoke()
            pendingAction = null
        }
    }

    Scaffold(
        containerColor = MaterialTheme.colorScheme.background
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 16.dp),
            contentPadding = PaddingValues(bottom = 24.dp)
        ) {
            item {
                Spacer(modifier = Modifier.height(24.dp))
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Column {
                        Text("Share Offline", fontWeight = FontWeight.Bold, fontSize = 28.sp, color = MaterialTheme.colorScheme.onBackground)
                        Spacer(modifier = Modifier.height(4.dp))
                        Text("Send and receive without internet", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp)
                    }
                    Box(
                        modifier = Modifier.size(48.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary.copy(alpha = 0.1f)),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.Default.WifiTethering, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                    }
                }
                Spacer(modifier = Modifier.height(32.dp))
            }

            // Main Actions
            item {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                    // Send Card
                    Card(
                        modifier = Modifier
                            .weight(1f)
                            .clickable {
                                checkPermissionsAndRun {
                                    showSendDialog = true
                                    p2pManager.startDiscovery()
                                }
                            },
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primary),
                        shape = RoundedCornerShape(24.dp)
                    ) {
                        Column(modifier = Modifier.padding(24.dp), horizontalAlignment = Alignment.Start) {
                            Box(modifier = Modifier.size(48.dp).clip(CircleShape).background(Color.White.copy(alpha = 0.2f)), contentAlignment = Alignment.Center) {
                                Icon(Icons.Default.ArrowUpward, contentDescription = "Send", tint = Color.White)
                            }
                            Spacer(modifier = Modifier.height(16.dp))
                            Text("Send", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 20.sp)
                            Text("Share content", color = Color.White.copy(alpha = 0.8f), fontSize = 12.sp)
                        }
                    }

                    // Receive Card
                    Card(
                        modifier = Modifier
                            .weight(1f)
                            .clickable {
                                checkPermissionsAndRun {
                                    showReceiveDialog = true
                                    p2pManager.startAdvertising(Build.MODEL)
                                }
                            },
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
                        shape = RoundedCornerShape(24.dp)
                    ) {
                        Column(modifier = Modifier.padding(24.dp), horizontalAlignment = Alignment.Start) {
                            Box(modifier = Modifier.size(48.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary.copy(alpha = 0.1f)), contentAlignment = Alignment.Center) {
                                Icon(Icons.Default.ArrowDownward, contentDescription = "Receive", tint = MaterialTheme.colorScheme.primary)
                            }
                            Spacer(modifier = Modifier.height(16.dp))
                            Text("Receive", color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold, fontSize = 20.sp)
                            Text("Get from others", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
                        }
                    }
                }
                Spacer(modifier = Modifier.height(32.dp))
            }

            // Transfer Progress
            if (p2pState == P2PState.TRANSFERRING) {
                item {
                    Column(modifier = Modifier.fillMaxWidth().padding(vertical = 12.dp)) {
                        Text("Transferring File...", color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                        Spacer(modifier = Modifier.height(8.dp))
                        LinearProgressIndicator(
                            progress = { transferProgress },
                            modifier = Modifier.fillMaxWidth().height(8.dp).clip(RoundedCornerShape(4.dp)),
                            color = MaterialTheme.colorScheme.primary,
                            trackColor = MaterialTheme.colorScheme.surfaceVariant
                        )
                        Spacer(modifier = Modifier.height(4.dp))
                        Text("${(transferProgress * 100).toInt()}%", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, modifier = Modifier.fillMaxWidth(), textAlign = TextAlign.End)
                    }
                }
            }

            // Tips section
            item {
                Spacer(modifier = Modifier.height(24.dp))
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.2f)),
                    border = borderStroke()
                ) {
                    Row(modifier = Modifier.padding(16.dp)) {
                        Box(
                            modifier = Modifier.size(32.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary.copy(alpha = 0.1f)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Outlined.Shield, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(16.dp))
                        }
                        Spacer(modifier = Modifier.width(12.dp))
                        Column {
                            Text("High-Speed Wi-Fi Direct", color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                            Spacer(modifier = Modifier.height(4.dp))
                            Text("Files are sent using ultra-fast Wi-Fi Direct (up to 5GHz) for large 4K movies.", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, lineHeight = 18.sp)
                        }
                    }
                }
            }
        }
    }

    var selectedFolder by remember { mutableStateOf<String?>(null) }
    
    if (showSendDialog) {
        AlertDialog(
            onDismissRequest = {
                showSendDialog = false
                selectedFolder = null
                p2pManager.stopAll()
            },
            title = { Text(if (selectedFolder == null) "Select Media to Send" else selectedFolder!!, fontWeight = FontWeight.Bold) },
            text = {
                Column {
                    if (p2pState == P2PState.DISCOVERING && discoveredEndpoints.isEmpty()) {
                        CircularProgressIndicator(modifier = Modifier.align(Alignment.CenterHorizontally).padding(16.dp))
                        Text("Looking for devices...", textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth())
                    } else if (discoveredEndpoints.isNotEmpty() && connectedEndpoint == null) {
                        Text("Available Devices:", fontWeight = FontWeight.Bold, modifier = Modifier.padding(vertical = 8.dp))
                        discoveredEndpoints.forEach { endpoint ->
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clickable { p2pManager.requestConnection(endpoint.id, Build.MODEL) }
                                    .padding(vertical = 8.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(Icons.Default.PhoneAndroid, contentDescription = null)
                                Spacer(modifier = Modifier.width(16.dp))
                                Text(endpoint.name)
                            }
                        }
                    } else if (connectedEndpoint != null) {
                        Text("Connected to ${connectedEndpoint?.name}", color = Color.Green, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        LazyColumn(modifier = Modifier.fillMaxWidth().heightIn(max = 300.dp)) {
                            if (completedDownloads.isEmpty()) {
                                item { Text("No downloaded movies found.", color = MaterialTheme.colorScheme.onSurfaceVariant) }
                            } else {
                                if (selectedFolder == null) {
                                    // Group by Type/Title
                                    val movies = completedDownloads.filter { it.isMovie }
                                    val series = completedDownloads.filter { !it.isMovie }
                                    
                                    if (movies.isNotEmpty()) {
                                        item { Text("Movies", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(vertical = 8.dp)) }
                                        items(movies) { item ->
                                            SendItemRow(item, context, p2pManager, connectedEndpoint) { 
                                                showSendDialog = false 
                                                selectedFolder = null
                                            }
                                        }
                                    }
                                    
                                    if (series.isNotEmpty()) {
                                        item { Text("Series / Anime", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(vertical = 8.dp)) }
                                        
                                        // Group series by title (creating folders)
                                        val groupedSeries = series.groupBy { it.title.split(" - ").firstOrNull() ?: it.title }
                                        
                                        items(groupedSeries.keys.toList()) { folderName ->
                                            Row(
                                                modifier = Modifier
                                                    .fillMaxWidth()
                                                    .clickable { selectedFolder = folderName }
                                                    .padding(vertical = 12.dp, horizontal = 8.dp),
                                                verticalAlignment = Alignment.CenterVertically
                                            ) {
                                                Icon(Icons.Outlined.Folder, contentDescription = "Folder", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(32.dp))
                                                Spacer(modifier = Modifier.width(16.dp))
                                                Column(modifier = Modifier.weight(1f)) {
                                                    Text(folderName, color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
                                                    Text("${groupedSeries[folderName]?.size ?: 0} Episodes", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
                                                }
                                                Icon(Icons.AutoMirrored.Filled.ArrowForward, contentDescription = "Open", tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(16.dp))
                                            }
                                        }
                                    }
                                } else {
                                    // Inside a folder
                                    item {
                                        Row(
                                            modifier = Modifier.fillMaxWidth().clickable { selectedFolder = null }.padding(vertical = 8.dp),
                                            verticalAlignment = Alignment.CenterVertically
                                        ) {
                                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = MaterialTheme.colorScheme.primary)
                                            Spacer(modifier = Modifier.width(8.dp))
                                            Text("Back to Folders", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                                        }
                                    }
                                    
                                    val folderItems = completedDownloads.filter { !it.isMovie && (it.title.split(" - ").firstOrNull() ?: it.title) == selectedFolder }
                                    items(folderItems) { item ->
                                        SendItemRow(item, context, p2pManager, connectedEndpoint) { 
                                            showSendDialog = false 
                                            selectedFolder = null
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = {
                    showSendDialog = false
                    selectedFolder = null
                    p2pManager.stopAll()
                }) { Text("Cancel") }
            }
        )
    }

    if (showReceiveDialog) {
        AlertDialog(
            onDismissRequest = {
                showReceiveDialog = false
                p2pManager.stopAll()
            },
            title = { Text("Receive Media", fontWeight = FontWeight.Bold) },
            text = {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    if (connectedEndpoint != null) {
                        Icon(Icons.Default.CheckCircle, contentDescription = null, tint = Color.Green, modifier = Modifier.size(64.dp))
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("Connected to ${connectedEndpoint!!.name}", fontWeight = FontWeight.Bold)
                        Text("Waiting for files...", color = MaterialTheme.colorScheme.onSurfaceVariant)
                    } else {
                        // Fake QR Code visually
                        Box(
                            modifier = Modifier
                                .size(200.dp)
                                .background(Color.White, RoundedCornerShape(16.dp))
                                .padding(16.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Outlined.QrCode2, contentDescription = "QR Code", tint = Color.Black, modifier = Modifier.fillMaxSize())
                        }
                        Spacer(modifier = Modifier.height(24.dp))
                        CircularProgressIndicator(modifier = Modifier.size(24.dp), strokeWidth = 2.dp)
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("Ready to receive", fontWeight = FontWeight.Bold, fontSize = 18.sp)
                        Text("Make sure the sender is on the same Wi-Fi network or Bluetooth is enabled. Transfer uses high-speed Wi-Fi Direct.", textAlign = TextAlign.Center, color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, modifier = Modifier.padding(horizontal = 16.dp))
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = {
                    showReceiveDialog = false
                    p2pManager.stopAll()
                }) { Text("Cancel") }
            }
        )
    }
}

@Composable
fun SendItemRow(item: DownloadItem, context: android.content.Context, p2pManager: P2PManager, connectedEndpoint: Endpoint?, onSent: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable {
                val file = File(context.filesDir, "downloads/${item.id}.mp4")
                if (file.exists() && connectedEndpoint != null) {
                    p2pManager.sendMovie(connectedEndpoint.id, item.id, item.title, item.isMovie, item.posterUrl, file)
                }
                onSent()
            }
            .padding(vertical = 12.dp, horizontal = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(Icons.Outlined.Movie, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
        Spacer(modifier = Modifier.width(16.dp))
        Column {
            Text(item.title, color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
            Text(if (item.isMovie) "Movie" else "Episode", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
        }
        Spacer(modifier = Modifier.weight(1f))
        Icon(Icons.AutoMirrored.Filled.Send, contentDescription = "Send", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(18.dp))
    }
}

@Composable
private fun borderStroke() = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
