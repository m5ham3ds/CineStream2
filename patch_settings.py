import re

with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "r") as f:
    content = f.read()

preferences_code = """
        Spacer(modifier = Modifier.height(32.dp))
        SettingsSectionHeader(icon = Icons.Outlined.Settings, title = "Advanced Preferences")
        Column(modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(12.dp)).background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))) {
            SettingsListItem(Icons.Outlined.PlayCircleOutline, "Playback", "Quality, subtitles, autoplay", false) {}
            SettingsListItem(Icons.Outlined.Download, "Downloads", "Wi-Fi only, smart downloads", false) {}
            SettingsListItem(Icons.Outlined.Settings, "Notifications", "Manage your notification preferences", true) {}
        }
        
        Spacer(modifier = Modifier.height(100.dp))"""

if "Advanced Preferences" not in content:
    content = content.replace("Spacer(modifier = Modifier.height(100.dp))", preferences_code)
    
    with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "w") as f:
        f.write(content)

