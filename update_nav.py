import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Add new routes
if "const val ROUTE_SECURITY" not in content:
    content = content.replace("const val ROUTE_EDIT_PROFILE = \"edit_profile\"", "const val ROUTE_EDIT_PROFILE = \"edit_profile\"\nconst val ROUTE_SECURITY = \"security\"\nconst val ROUTE_SUBSCRIPTION = \"subscription\"\nconst val ROUTE_SETTINGS = \"settings\"")

# Update ProfileScreen call
old_profile = """ProfileScreen(
                        onNavigateToEditProfile = { navController.navigate(ROUTE_EDIT_PROFILE) },
                        onNavigateToSubscription = { /* TODO */ }
                    )"""
new_profile = """ProfileScreen(
                        onNavigateToEditProfile = { navController.navigate(ROUTE_EDIT_PROFILE) },
                        onNavigateToSubscription = { navController.navigate(ROUTE_SUBSCRIPTION) },
                        onNavigateToSecurity = { navController.navigate(ROUTE_SECURITY) },
                        onNavigateToSettings = { navController.navigate(ROUTE_SETTINGS) }
                    )"""
content = content.replace(old_profile, new_profile)

# Add destinations
new_destinations = """        composable(ROUTE_SECURITY) {
            com.example.ui.screens.profile.SecurityScreen(onBack = { navController.popBackStack() })
        }
        composable(ROUTE_SUBSCRIPTION) {
            com.example.ui.screens.profile.SubscriptionScreen(onBack = { navController.popBackStack() })
        }
        composable(ROUTE_SETTINGS) {
            com.example.ui.screens.profile.SettingsScreen(onBack = { navController.popBackStack() })
        }"""
        
if "ROUTE_SECURITY" not in content:
    content = content.replace("composable(ROUTE_EDIT_PROFILE) {", new_destinations + "\n        composable(ROUTE_EDIT_PROFILE) {")

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
