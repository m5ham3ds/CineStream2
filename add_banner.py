import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

old_bb = """            bottomBar = {
                if (bottomBarRoutes.contains(currentRoute)) {
                    BottomNavBar(navController = navController)
                }
            }"""

new_bb = """            bottomBar = {
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

if old_bb in content:
    content = content.replace(old_bb, new_bb)
else:
    print("Not found!")

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
