with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

old_download = """    if (showDownloadSheet) {
        DownloadQualitySheet(
            onDismiss = { showDownloadSheet = false },
            onQualitySelected = { quality ->
                android.widget.Toast.makeText(context, "Downloading in $quality...", android.widget.Toast.LENGTH_SHORT).show()
                showDownloadSheet = false
            }
        )
    }"""
new_download = """    if (showDownloadSheet) {
        DownloadQualitySheet(
            onDismiss = { showDownloadSheet = false },
            onQualitySelected = { quality ->
                uiState.currentVideoUrl?.let { videoUrl ->
                    com.example.utils.AndroidDownloader.downloadVideo(context, videoUrl, "${uiState.title} - $quality")
                } ?: run {
                    android.widget.Toast.makeText(context, "Please wait for the stream to load first.", android.widget.Toast.LENGTH_SHORT).show()
                }
                showDownloadSheet = false
            }
        )
    }"""

content = content.replace(old_download, new_download)

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)
