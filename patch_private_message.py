import re

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "r") as f:
    content = f.read()

pm_old = """data class PrivateMessage(
    val id: String = "",
    val senderId: String = "",
    val text: String = "",
    val timestamp: Long = System.currentTimeMillis()
)"""

pm_new = """data class PrivateMessage(
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

content = content.replace(pm_old, pm_new)

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "w") as f:
    f.write(content)
