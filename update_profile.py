import re

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "r") as f:
    content = f.read()

# Update signature
old_sig = "fun ProfileScreen(onNavigateToEditProfile: () -> Unit, onNavigateToSubscription: () -> Unit) {"
new_sig = "fun ProfileScreen(\n    onNavigateToEditProfile: () -> Unit,\n    onNavigateToSubscription: () -> Unit,\n    onNavigateToSecurity: () -> Unit,\n    onNavigateToSettings: () -> Unit\n) {"
content = content.replace(old_sig, new_sig)

# Update the Account list
old_account = """        // Account
        Text("Account", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(12.dp))
        Column(modifier = Modifier.fillMaxWidth().background(cardColor, RoundedCornerShape(12.dp))) {
            ProfileListItem(Icons.Default.Person, "Account Information", "Update your personal details", false, primaryRed, iconBgColor)
            ProfileListItem(Icons.Outlined.Security, "Security", "Password, device management", false, primaryRed, iconBgColor)
            ProfileListItem(Icons.Outlined.CreditCard, "Subscription", "Manage your plan and billing", true, primaryRed, iconBgColor)
        }"""
new_account = """        // Account
        Text("Account", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(12.dp))
        Column(modifier = Modifier.fillMaxWidth().background(cardColor, RoundedCornerShape(12.dp))) {
            ProfileListItem(Icons.Default.Person, "Account Information", "Update your personal details", false, primaryRed, iconBgColor, onClick = onNavigateToEditProfile)
            ProfileListItem(Icons.Outlined.Security, "Security", "Password, device management", false, primaryRed, iconBgColor, onClick = onNavigateToSecurity)
            ProfileListItem(Icons.Outlined.CreditCard, "Subscription", "Manage your plan and billing", false, primaryRed, iconBgColor, onClick = onNavigateToSubscription)
            ProfileListItem(Icons.Outlined.Settings, "Settings", "App preferences and settings", true, primaryRed, iconBgColor, onClick = onNavigateToSettings)
        }"""
content = content.replace(old_account, new_account)

# Remove Preferences
old_pref = """        Spacer(modifier = Modifier.height(24.dp))
        // Preferences
        Text("Preferences", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(12.dp))
        Column(modifier = Modifier.fillMaxWidth().background(cardColor, RoundedCornerShape(12.dp))) {
            ProfileListItem(Icons.Outlined.Settings, "App Settings", "Customize your experience", false, primaryRed, iconBgColor)
            ProfileListItem(Icons.Outlined.PlayCircleOutline, "Playback", "Quality, subtitles, autoplay", false, primaryRed, iconBgColor)
            ProfileListItem(Icons.Outlined.Notifications, "Notifications", "Manage your notification preferences", true, primaryRed, iconBgColor)
        }"""
content = content.replace(old_pref, "")

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write(content)

