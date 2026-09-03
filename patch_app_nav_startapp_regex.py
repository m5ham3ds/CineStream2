import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Replace all navigate to MovieDetails with Ad + Navigate
content = re.sub(
    r'onMovieClick\s*=\s*\{([^}]*?)navController\.navigate\(Screen\.MovieDetails\.createRoute\((.*?)\)\)(.*?)\}',
    r'onMovieClick = { \1com.example.utils.AdManager.showInterstitial(context)\nnavController.navigate(Screen.MovieDetails.createRoute(\2))\3}',
    content
)

content = re.sub(
    r'onSeriesClick\s*=\s*\{([^}]*?)navController\.navigate\(Screen\.SeriesDetails\.createRoute\((.*?)\)\)(.*?)\}',
    r'onSeriesClick = { \1com.example.utils.AdManager.showInterstitial(context)\nnavController.navigate(Screen.SeriesDetails.createRoute(\2))\3}',
    content
)

content = re.sub(
    r'onAnimeClick\s*=\s*\{([^}]*?)navController\.navigate\(Screen\.SeriesDetails\.createRoute\((.*?)\)\)(.*?)\}',
    r'onAnimeClick = { \1com.example.utils.AdManager.showInterstitial(context)\nnavController.navigate(Screen.SeriesDetails.createRoute(\2))\3}',
    content
)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)

