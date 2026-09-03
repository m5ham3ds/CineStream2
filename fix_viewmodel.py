with open("app/src/main/java/com/example/ui/screens/social/SocialViewModel.kt", "r") as f:
    content = f.read()

content = content.replace(
"""    fun addStory(imageUrl: String) {
        if (imageUrl.isNotBlank()) {
            repo.addStory(imageUrl)
        }
    }""",
"""    fun addStory(imageUrl: String) {
        if (imageUrl.isNotBlank()) {
            viewModelScope.launch { repo.addStory(imageUrl) }
        }
    }""")

with open("app/src/main/java/com/example/ui/screens/social/SocialViewModel.kt", "w") as f:
    f.write(content)
