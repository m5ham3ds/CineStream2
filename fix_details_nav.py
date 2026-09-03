import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Update the calls to navController.navigate("player?...")
# MovieDetailsScreen
old_movie_nav = """                                val encodedUrl = URLEncoder.encode(url, "UTF-8")
                                val encodedTitle = URLEncoder.encode(title, "UTF-8")
                                navController.navigate("player?url=$encodedUrl&title=$encodedTitle")"""
new_movie_nav = """                                val encodedUrl = URLEncoder.encode(url, "UTF-8")
                                val encodedTitle = URLEncoder.encode(title, "UTF-8")
                                navController.navigate("player?mediaId=$movieId&isMovie=true&title=$encodedTitle&url=$encodedUrl")"""
content = content.replace(old_movie_nav, new_movie_nav)

# SeriesDetailsScreen
old_series_nav = """                                val encodedUrl = URLEncoder.encode(url, "UTF-8")
                                val encodedTitle = URLEncoder.encode(title, "UTF-8")
                                navController.navigate("player?url=$encodedUrl&title=$encodedTitle")"""
new_series_nav = """                                val encodedUrl = URLEncoder.encode(url, "UTF-8")
                                val encodedTitle = URLEncoder.encode(title, "UTF-8")
                                navController.navigate("player?mediaId=$seriesId&isMovie=false&title=$encodedTitle&url=$encodedUrl")"""
content = content.replace(old_series_nav, new_series_nav)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)

