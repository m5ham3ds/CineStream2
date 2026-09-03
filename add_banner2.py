import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

content = re.sub(
    r'bottomBar\s*=\s*\{\s*if\s*\(bottomBarRoutes\.contains\(currentRoute\)\)\s*\{\s*BottomNavBar\(navController\s*=\s*navController\)\s*\}\s*\}',
    r'''bottomBar = {
                androidx.compose.foundation.layout.Column {
                    if (currentRoute != null && currentRoute != Screen.Splash.route && currentRoute != Screen.Auth.route && currentRoute != Screen.Onboarding.route) {
                        if (!currentRoute.contains("movie_details") && !currentRoute.contains("series_details")) {
                            com.example.ui.components.StartAppBanner()
                        }
                    }
                    if (bottomBarRoutes.contains(currentRoute)) {
                        BottomNavBar(navController = navController)
                    }
                }
            }''',
    content
)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
