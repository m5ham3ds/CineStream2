import re

with open("app/src/main/java/com/example/navigation/Screen.kt", "r") as f:
    content = f.read()

if "object Security :" not in content:
    content = content.replace("object Settings : Screen(\"settings\", \"Settings\", Icons.Default.Settings)", 
    "object Settings : Screen(\"settings\", \"Settings\", Icons.Default.Settings)\n    object Security : Screen(\"security\", \"Security\", Icons.Default.Person)\n    object Subscription : Screen(\"subscription\", \"Subscription\", Icons.Default.Person)")
    
    with open("app/src/main/java/com/example/navigation/Screen.kt", "w") as f:
        f.write(content)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Import the new screens
if "import com.example.ui.screens.profile.SecurityScreen" not in content:
    content = content.replace("import com.example.ui.screens.profile.EditProfileScreen",
    "import com.example.ui.screens.profile.EditProfileScreen\nimport com.example.ui.screens.profile.SecurityScreen\nimport com.example.ui.screens.profile.SubscriptionScreen")

# Add the composables
new_routes = """
                composable(Screen.Security.route) {
                    SecurityScreen(onBack = { navController.popBackStack() })
                }
                composable(Screen.Subscription.route) {
                    SubscriptionScreen(onBack = { navController.popBackStack() })
                }
"""
if "composable(Screen.Security.route)" not in content:
    content = content.replace("composable(Screen.Settings.route) {", new_routes + "\n                composable(Screen.Settings.route) {")

# Update ProfileScreen instantiation
profile_old = """ProfileScreen(
                        onNavigateToAuth = {
                            navController.navigate(Screen.Auth.route) {
                                popUpTo(Screen.Home.route) { inclusive = false }
                            }
                        },
                        onNavigateToEditProfile = {
                            navController.navigate(Screen.EditProfile.route)
                        }
                    )"""
profile_new = """ProfileScreen(
                        onNavigateToAuth = {
                            navController.navigate(Screen.Auth.route) {
                                popUpTo(Screen.Home.route) { inclusive = false }
                            }
                        },
                        onNavigateToEditProfile = {
                            navController.navigate(Screen.EditProfile.route)
                        },
                        onNavigateToSecurity = {
                            navController.navigate(Screen.Security.route)
                        },
                        onNavigateToSubscription = {
                            navController.navigate(Screen.Subscription.route)
                        }
                    )"""
content = content.replace(profile_old, profile_new)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)

