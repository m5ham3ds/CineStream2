with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

# For Movie
old_movie_download = """                        if (isDownloadMode) {
                            scope.launch {
                                downloadRepository.addToDownloads(DownloadItem(
                                    id = movie.id, title = movie.title, posterUrl = movie.posterUrl, isMovie = true, quality = source.quality
                                ))
                                Toast.makeText(context, "Download Started", Toast.LENGTH_SHORT).show()
                            }
                        } else {"""
new_movie_download = """                        if (isDownloadMode) {
                            scope.launch {
                                downloadRepository.addToDownloads(DownloadItem(
                                    id = movie.id, title = movie.title, posterUrl = movie.posterUrl, isMovie = true, quality = source.quality
                                ))
                                com.example.utils.AndroidDownloader.downloadVideo(ctx, source.url, "${movie.title} - ${source.quality}")
                            }
                        } else {"""
content = content.replace(old_movie_download, new_movie_download)

# For Series
old_series_download = """                        if (isDownloadMode) {
                            scope.launch {
                                downloadRepository.addToDownloads(DownloadItem(
                                    id = ep.id, title = "${series.title} - S${uiState.selectedSeason?.seasonNumber}E${ep.episodeNumber}", posterUrl = ep.thumbnailUrl, isMovie = false, quality = source.quality
                                ))
                                Toast.makeText(context, "Download Started: ${source.providerName}", Toast.LENGTH_SHORT).show()
                            }
                        } else {"""
new_series_download = """                        if (isDownloadMode) {
                            scope.launch {
                                val fullTitle = "${series.title} - S${uiState.selectedSeason?.seasonNumber}E${ep.episodeNumber}"
                                downloadRepository.addToDownloads(DownloadItem(
                                    id = ep.id, title = fullTitle, posterUrl = ep.thumbnailUrl, isMovie = false, quality = source.quality
                                ))
                                com.example.utils.AndroidDownloader.downloadVideo(context, source.url, "$fullTitle - ${source.quality}")
                            }
                        } else {"""
content = content.replace(old_series_download, new_series_download)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
