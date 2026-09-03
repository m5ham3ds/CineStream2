with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Replace the specific bad string
content = content.replace(
    'navController.navigate("player?mediaId=$movieId&isMovie=true&title=$encodedTitle&url=$encodedUrl")',
    'navController.navigate("player?mediaId=$seriesId&isMovie=false&title=$encodedTitle&url=$encodedUrl")',
    1 # but we want to replace the SECOND occurrence
)
