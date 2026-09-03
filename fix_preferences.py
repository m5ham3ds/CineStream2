import re

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "r") as f:
    content = f.read()

# Let's remove the Preferences block
pattern = r"\s*Spacer\(modifier = Modifier\.height\(24\.dp\)\)\s*// Preferences\s*Text\(\"Preferences\", color = Color\.White, fontSize = 20\.sp, fontWeight = FontWeight\.Bold\)\s*Spacer\(modifier = Modifier\.height\(12\.dp\)\)\s*Column\(modifier = Modifier\.fillMaxWidth\(\)\.background\(cardColor, RoundedCornerShape\(12\.dp\)\)\) \{\s*ProfileListItem\(Icons\.Outlined\.Settings, \"App Settings\", \"Customize your experience\", false, primaryRed, iconBgColor\)\s*ProfileListItem\(Icons\.Outlined\.PlayCircleOutline, \"Playback\", \"Quality, subtitles, autoplay\", false, primaryRed, iconBgColor\)\s*ProfileListItem\(Icons\.Outlined\.Notifications, \"Notifications\", \"Manage your notification preferences\", true, primaryRed, iconBgColor\)\s*\}"

content = re.sub(pattern, "", content)

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write(content)
