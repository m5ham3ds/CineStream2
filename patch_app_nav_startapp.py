import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Add StartAppBanner to the bottom bar
bottom_bar_old = """            bottomBar = {
                if (bottomBarRoutes.contains(currentRoute)) {
                    BottomNavBar(navController = navController)
                }
       
        }"""

bottom_bar_new = """            bottomBar = {
                Column {
                    if (currentRoute != null && currentRoute != Screen.Splash.route && currentRoute != Screen.Auth.route && currentRoute != Screen.Onboarding.route) {
                        if (!currentRoute.contains("movie_details") && !currentRoute.contains("series_details")) {
                            com.example.ui.components.StartAppBanner()
                        }
                    }
                    if (bottomBarRoutes.contains(currentRoute)) {
                        BottomNavBar(navController = navController)
                    }
                }
            }"""

if bottom_bar_old in content:
    content = content.replace(bottom_bar_old, bottom_bar_new)

# Add Interstitial to Navigation Actions
# E.g. onMovieClick = { movieId -> ... }
nav_actions_replacements = [
    (
        "onMovieClick = { movieId ->\n                    navController.navigate(Screen.MovieDetails.createRoute(movieId))\n                }",
        "onMovieClick = { movieId ->\n                    com.example.utils.AdManager.showInterstitial(context)\n                    navController.navigate(Screen.MovieDetails.createRoute(movieId))\n                }"
    ),
    (
        "onSeriesClick = { seriesId ->\n                    navController.navigate(Screen.SeriesDetails.createRoute(seriesId))\n                }",
        "onSeriesClick = { seriesId ->\n                    com.example.utils.AdManager.showInterstitial(context)\n                    navController.navigate(Screen.SeriesDetails.createRoute(seriesId))\n                }"
    ),
    (
        "onAnimeClick = { seriesId ->\n                    navController.navigate(Screen.SeriesDetails.createRoute(seriesId))\n                }",
        "onAnimeClick = { seriesId ->\n                    com.example.utils.AdManager.showInterstitial(context)\n                    navController.navigate(Screen.SeriesDetails.createRoute(seriesId))\n                }"
    )
]

for old, new in nav_actions_replacements:
    content = content.replace(old, new)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)

