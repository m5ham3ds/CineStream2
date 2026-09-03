with open("app/src/main/java/com/example/ui/screens/social/ChatViewModel.kt", "r") as f:
    content = f.read()

new_methods = """
    fun editMessage(msgId: String, newText: String) {
        if (currentConversationId.isNotEmpty() && newText.isNotBlank()) {
            repo.editMessage(currentConversationId, msgId, newText)
        }
    }

    fun deleteMessage(msgId: String, forEveryone: Boolean) {
        if (currentConversationId.isNotEmpty()) {
            repo.deleteMessage(currentConversationId, msgId, forEveryone)
        }
    }

    fun reactToMessage(msgId: String, emoji: String) {
        if (currentConversationId.isNotEmpty()) {
            repo.reactToMessage(currentConversationId, msgId, emoji)
        }
    }

    fun sendVoiceMessage(voicePath: String) {
        if (currentConversationId.isNotEmpty()) {
            repo.sendVoiceMessage(currentConversationId, voicePath)
        }
    }
}
"""

last_brace_index = content.rfind("}")
if last_brace_index != -1:
    content = content[:last_brace_index] + new_methods + "\n"

with open("app/src/main/java/com/example/ui/screens/social/ChatViewModel.kt", "w") as f:
    f.write(content)
