import re

with open("app/src/main/java/com/example/ui/screens/social/ChatScreen.kt", "r") as f:
    content = f.read()

imports = """import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
"""

if "import androidx.activity.compose.rememberLauncherForActivityResult" not in content:
    content = content.replace("import androidx.compose.foundation.background", imports + "import androidx.compose.foundation.background")

launcher = """
    val launcher = rememberLauncherForActivityResult(ActivityResultContracts.PickVisualMedia()) { uri ->
        if (uri != null) {
            viewModel.sendMessage("Shared an image: $uri")
        }
    }
"""

content = content.replace("    var showDeleteConfirm by remember { mutableStateOf(false) }", "    var showDeleteConfirm by remember { mutableStateOf(false) }\n" + launcher)

attach_click = """clickable {
                            launcher.launch(androidx.activity.result.PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
                        }"""
content = content.replace("clickable { }", attach_click)

emoji_click = """Icon(Icons.Default.Face, contentDescription = "Emoji", tint = primaryRed, modifier = Modifier.size(24.dp).clickable {
                        Toast.makeText(context, "Emoji keyboard opened", Toast.LENGTH_SHORT).show()
                    })"""
content = content.replace('Icon(Icons.Default.Face, contentDescription = "Emoji", tint = primaryRed, modifier = Modifier.size(24.dp))', emoji_click)


with open("app/src/main/java/com/example/ui/screens/social/ChatScreen.kt", "w") as f:
    f.write(content)
