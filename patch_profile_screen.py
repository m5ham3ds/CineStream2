import re

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "r") as f:
    content = f.read()

sig_old = "fun ProfileScreen(onNavigateToAuth: () -> Unit = {}, onNavigateToEditProfile: () -> Unit = {}) {"
sig_new = "fun ProfileScreen(onNavigateToAuth: () -> Unit = {}, onNavigateToEditProfile: () -> Unit = {}, onNavigateToSecurity: () -> Unit = {}, onNavigateToSubscription: () -> Unit = {}) {"
content = content.replace(sig_old, sig_new)

# Edit profile pencil / avatar
old_avatar = """Box(
                modifier = Modifier.size(80.dp).clip(CircleShape).background(Color.DarkGray).border(2.dp, primaryRed, CircleShape),
                contentAlignment = Alignment.Center
            ) {
                if (currentUser?.photoUrl?.isNotEmpty() == true) {
                    AsyncImage(
                        model = currentUser?.photoUrl,
                        contentDescription = "Profile Picture",
                        modifier = Modifier.fillMaxSize(),
                        contentScale = ContentScale.Crop
                    )
                } else {
                    Text(currentUser?.username?.firstOrNull()?.uppercase() ?: "U", color = Color.White, fontSize = 32.sp, fontWeight = FontWeight.Bold)
                }
                Box(
                    modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = 0.3f)).clickable { onNavigateToEditProfile() },
                    contentAlignment = Alignment.Center
                ) {
                    Icon(Icons.Default.Edit, contentDescription = "Edit Profile", tint = Color.White, modifier = Modifier.size(24.dp))
                }
            }"""

if old_avatar not in content:
    # Need to find the exact avatar code
    pass

# We also need to change ProfileListItem to take onClick parameter
old_list_item = """@Composable
fun ProfileListItem(icon: ImageVector, title: String, subtitle: String, isLast: Boolean, tintColor: Color, iconBg: Color) {
    Row(
        modifier = Modifier.fillMaxWidth().clickable { }.padding(16.dp),"""
new_list_item = """@Composable
fun ProfileListItem(icon: ImageVector, title: String, subtitle: String, isLast: Boolean, tintColor: Color, iconBg: Color, onClick: () -> Unit = {}) {
    Row(
        modifier = Modifier.fillMaxWidth().clickable { onClick() }.padding(16.dp),"""
content = content.replace(old_list_item, new_list_item)

# Manage Plan Button
manage_plan_old = """Button(
                onClick = {},
                colors = ButtonDefaults.buttonColors(containerColor = primaryRed),"""
manage_plan_new = """Button(
                onClick = onNavigateToSubscription,
                colors = ButtonDefaults.buttonColors(containerColor = primaryRed),"""
content = content.replace(manage_plan_old, manage_plan_new)

# Account & Preferences sections
account_pref_old_start = """// Account
        Text("Account", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(12.dp))
        Column(modifier = Modifier.fillMaxWidth().background(cardColor, RoundedCornerShape(12.dp))) {
            ProfileListItem(Icons.Default.Person, "Account Information", "Update your personal details", false, primaryRed, iconBgColor)
            ProfileListItem(Icons.Outlined.Security, "Security", "Password, device management", false, primaryRed, iconBgColor)
            ProfileListItem(Icons.Outlined.CreditCard, "Subscription", "Manage your plan and billing", true, primaryRed, iconBgColor)
        }
        Spacer(modifier = Modifier.height(24.dp))
        // Preferences
        Text("Preferences", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(12.dp))
        Column(modifier = Modifier.fillMaxWidth().background(cardColor, RoundedCornerShape(12.dp))) {
            ProfileListItem(Icons.Outlined.Settings, "App Settings", "Customize your experience", false, primaryRed, iconBgColor)
            ProfileListItem(Icons.Outlined.PlayCircleOutline, "Playback", "Quality, subtitles, autoplay", false, primaryRed, iconBgColor)
            ProfileListItem(Icons.Outlined.Notifications, "Notifications", "Manage your notification preferences", true, primaryRed, iconBgColor)
        }"""

account_new = """// Account
        Text("Account", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(12.dp))
        Column(modifier = Modifier.fillMaxWidth().background(cardColor, RoundedCornerShape(12.dp))) {
            ProfileListItem(Icons.Default.Person, "Account Information", "Update your personal details", false, primaryRed, iconBgColor, onClick = onNavigateToEditProfile)
            ProfileListItem(Icons.Outlined.Security, "Security", "Password, device management", false, primaryRed, iconBgColor, onClick = onNavigateToSecurity)
            ProfileListItem(Icons.Outlined.CreditCard, "Subscription", "Manage your plan and billing", true, primaryRed, iconBgColor, onClick = onNavigateToSubscription)
        }"""
content = content.replace(account_pref_old_start, account_new)

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write(content)

