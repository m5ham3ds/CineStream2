import re

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "r") as f:
    content = f.read()

content = content.replace(
    "fun ProfileScreen(onNavigateToAuth: () -> Unit = {}, onNavigateToEditProfile: () -> Unit = {}, onNavigateToSecurity: () -> Unit = {}, onNavigateToSubscription: () -> Unit = {}) {",
    "fun ProfileScreen(onNavigateToAuth: () -> Unit = {}, onNavigateToEditProfile: () -> Unit = {}, onNavigateToSecurity: () -> Unit = {}, onNavigateToSubscription: () -> Unit = {}, onNavigateToSettings: () -> Unit = {}) {"
)

# And also let's make sure we update AppNavigation.kt correctly if not done.
with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write(content)
