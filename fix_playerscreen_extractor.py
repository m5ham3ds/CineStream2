with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

old_call = """        uiState.extractionUrl?.let { url ->
            HiddenVideoExtractor(
                url = url,
                onVideoUrlFound = { extractedUrl ->
                    viewModel.setExtractedUrl(extractedUrl)
                }
            )
        }"""
new_call = """        uiState.extractionUrl?.let { url ->
            HiddenVideoExtractor(
                url = url,
                isMovie = uiState.isMovie,
                season = uiState.currentSeasonNumber,
                episode = uiState.currentEpisodeNumber,
                onVideoUrlFound = { extractedUrl ->
                    viewModel.setExtractedUrl(extractedUrl)
                }
            )
        }"""
content = content.replace(old_call, new_call)

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)
