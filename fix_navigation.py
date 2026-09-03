import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Update navigation route definition
old_route = """                composable("player?url={url}&title={title}") { backStackEntry ->
                    val url = backStackEntry.arguments?.getString("url") ?: return@composable
                    val title = backStackEntry.arguments?.getString("title") ?: "Unknown"
                    val decodedUrl = URLDecoder.decode(url, "UTF-8")
                    val decodedTitle = URLDecoder.decode(title, "UTF-8")
                    PlayerScreen(videoUrl = decodedUrl, title = decodedTitle, onBack = { navController.popBackStack() })
                }"""
new_route = """                composable("player?mediaId={mediaId}&isMovie={isMovie}&title={title}&url={url}") { backStackEntry ->
                    val mediaId = backStackEntry.arguments?.getString("mediaId") ?: ""
                    val isMovieStr = backStackEntry.arguments?.getString("isMovie") ?: "true"
                    val isMovie = isMovieStr.toBoolean()
                    val title = backStackEntry.arguments?.getString("title") ?: "Unknown"
                    val url = backStackEntry.arguments?.getString("url") ?: ""
                    
                    val decodedTitle = URLDecoder.decode(title, "UTF-8")
                    val decodedUrl = if (url.isNotEmpty()) URLDecoder.decode(url, "UTF-8") else ""
                    
                    com.example.ui.screens.player.PlayerScreen(
                        mediaId = mediaId, 
                        isMovie = isMovie, 
                        title = decodedTitle, 
                        onBack = { navController.popBackStack() }
                    )
                }"""
content = content.replace(old_route, new_route)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)

