import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

content = content.replace("import com.example.ui.screens.profile.ProfileScreen", 
"import com.example.ui.screens.profile.ProfileScreen\nimport com.example.ui.screens.profile.SecurityScreen\nimport com.example.ui.screens.profile.SubscriptionScreen\nimport com.example.ui.screens.profile.EditProfileScreen")

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
