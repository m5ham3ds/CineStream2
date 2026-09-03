import re

with open("app/src/main/java/com/example/ui/screens/social/SocialScreen.kt", "r") as f:
    content = f.read()

filter_old = """val filteredConversations = when (selectedCategory) {
                                "Unread" -> conversations.filter { 
                                    val otherUserId = it.participants.firstOrNull { p -> p != currentUser?.uid } ?: ""
                                    (it.unreadCounts[otherUserId] ?: 0) > 0 
                                }
                                else -> conversations
                            }"""

filter_new = """val filteredConversations = when (selectedCategory) {
                                "All Messages" -> conversations.filter { !it.isGroup && !it.isRequest }
                                "Unread" -> conversations.filter { (it.unreadCounts[currentUser?.uid ?: ""] ?: 0) > 0 }
                                "Groups" -> conversations.filter { it.isGroup }
                                "Requests" -> conversations.filter { it.isRequest }
                                else -> conversations
                            }"""

content = content.replace(filter_old, filter_new)

with open("app/src/main/java/com/example/ui/screens/social/SocialScreen.kt", "w") as f:
    f.write(content)

