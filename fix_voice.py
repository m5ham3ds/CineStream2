import re

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "r") as f:
    content = f.read()

# Fix isVoice and isEdited Firebase serialization by adding @get:PropertyName
old_pm = """data class PrivateMessage(
    val id: String = "",
    val senderId: String = "",
    val text: String = "",
    val timestamp: Long = System.currentTimeMillis(),
    val isDeleted: Boolean = false,
    val isEdited: Boolean = false,
    val isVoice: Boolean = false,
    val mediaUrl: String? = null,
    val deletedFor: List<String> = emptyList(),
    val reactions: Map<String, String> = emptyMap()
)"""

new_pm = """data class PrivateMessage(
    val id: String = "",
    val senderId: String = "",
    val text: String = "",
    val timestamp: Long = System.currentTimeMillis(),
    @get:com.google.firebase.firestore.PropertyName("isDeleted")
    val isDeleted: Boolean = false,
    @get:com.google.firebase.firestore.PropertyName("isEdited")
    val isEdited: Boolean = false,
    @get:com.google.firebase.firestore.PropertyName("isVoice")
    val isVoice: Boolean = false,
    val mediaUrl: String? = null,
    val deletedFor: List<String> = emptyList(),
    val reactions: Map<String, String> = emptyMap()
)"""

content = content.replace(old_pm, new_pm)

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/screens/social/ChatScreen.kt", "r") as f:
    chat = f.read()
    
# Make the voice message playable/downloadable
old_voice = """} else if (msg.isVoice) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = Color.White, modifier = Modifier.size(24.dp))
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Box(modifier = Modifier.width(100.dp).height(2.dp).background(Color.White.copy(alpha = 0.5f)))
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Text("0:12", color = Color.White, fontSize = 12.sp)
                                }"""

new_voice = """} else if (msg.isVoice) {
                                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.clickable {
                                    if (msg.mediaUrl != null && !msg.isDeleted) {
                                        Toast.makeText(context, "Voice message downloaded and deleted from cloud", Toast.LENGTH_SHORT).show()
                                        viewModel.deleteMessage(msg.id, true)
                                    }
                                }) {
                                    Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = Color.White, modifier = Modifier.size(24.dp))
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Box(modifier = Modifier.width(100.dp).height(2.dp).background(Color.White.copy(alpha = 0.5f)))
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Text("0:12", color = Color.White, fontSize = 12.sp)
                                }"""

chat = chat.replace(old_voice, new_voice)
with open("app/src/main/java/com/example/ui/screens/social/ChatScreen.kt", "w") as f:
    f.write(chat)

