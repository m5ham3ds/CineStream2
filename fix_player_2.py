import re

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

# Fix PlayerScreen signature
content = content.replace("fun PlayerScreen(mediaId: String, isMovie: Boolean, title: String, onBack: () -> Unit, viewModel: PlayerViewModel = androidx.lifecycle.viewmodel.compose.viewModel()) {", 
                          "fun PlayerScreen(mediaId: String, isMovie: Boolean, title: String, url: String? = null, onBack: () -> Unit, viewModel: PlayerViewModel = viewModel()) {")

content = content.replace("viewModel.initialize(mediaId, isMovie, title)", "viewModel.initialize(mediaId, isMovie, title, url)")

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)


with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "r") as f:
    content = f.read()

content = content.replace("fun initialize(mediaId: String, isMovie: Boolean, initialTitle: String) {", 
                          "fun initialize(mediaId: String, isMovie: Boolean, initialTitle: String, directUrl: String? = null) {")

content = content.replace("        if (!isMovie) {", """        if (!directUrl.isNullOrEmpty()) {
            _uiState.value = _uiState.value.copy(currentVideoUrl = directUrl, isLoading = false)
        } else if (!isMovie) {""")

with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "w") as f:
    f.write(content)
