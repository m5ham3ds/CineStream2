with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "r") as f:
    content = f.read()

new_methods = """
    fun editMessage(conversationId: String, msgId: String, newText: String) {
        val msgRef = db.collection("conversations").document(conversationId).collection("messages").document(msgId)
        msgRef.update("text", newText, "isEdited", true)
    }

    fun deleteMessage(conversationId: String, msgId: String, forEveryone: Boolean) {
        val user = getCurrentUser() ?: return
        val msgRef = db.collection("conversations").document(conversationId).collection("messages").document(msgId)
        if (forEveryone) {
            msgRef.update("isDeleted", true)
        } else {
            db.runTransaction { transaction ->
                val snapshot = transaction.get(msgRef)
                if (snapshot.exists()) {
                    val msg = snapshot.toObject(PrivateMessage::class.java)
                    if (msg != null) {
                        val newDeletedFor = msg.deletedFor.toMutableList()
                        if (!newDeletedFor.contains(user.uid)) {
                            newDeletedFor.add(user.uid)
                            transaction.update(msgRef, "deletedFor", newDeletedFor)
                        }
                    }
                }
            }
        }
    }

    fun reactToMessage(conversationId: String, msgId: String, emoji: String) {
        val user = getCurrentUser() ?: return
        val msgRef = db.collection("conversations").document(conversationId).collection("messages").document(msgId)
        db.runTransaction { transaction ->
            val snapshot = transaction.get(msgRef)
            if (snapshot.exists()) {
                val msg = snapshot.toObject(PrivateMessage::class.java)
                if (msg != null) {
                    val newReactions = msg.reactions.toMutableMap()
                    if (newReactions[user.uid] == emoji) {
                        newReactions.remove(user.uid)
                    } else {
                        newReactions[user.uid] = emoji
                    }
                    transaction.update(msgRef, "reactions", newReactions)
                }
            }
        }
    }

    fun sendVoiceMessage(conversationId: String, voicePath: String) {
        val user = getCurrentUser() ?: return
        val docRef = db.collection("conversations").document(conversationId)
        
        val msgRef = docRef.collection("messages").document()
        val msg = PrivateMessage(msgRef.id, user.uid, "Voice Message", System.currentTimeMillis(), isVoice = true, mediaUrl = voicePath)
        msgRef.set(msg)
        
        db.runTransaction { transaction ->
            val convSnapshot = transaction.get(docRef)
            if (convSnapshot.exists()) {
                val currentCountsAny = convSnapshot.get("unreadCounts")
                val currentCounts = if (currentCountsAny is Map<*, *>) {
                    currentCountsAny.entries.associate { it.key.toString() to (it.value.toString().toIntOrNull() ?: 0) }
                } else emptyMap()
                
                val newCounts = currentCounts.toMutableMap()
                val participantsAny = convSnapshot.get("participants")
                val participants = if (participantsAny is List<*>) {
                    participantsAny.map { it.toString() }
                } else emptyList()
                
                participants.forEach { p ->
                    if (p != user.uid) {
                        newCounts[p] = (newCounts[p] ?: 0) + 1
                    }
                }
                
                transaction.update(docRef, "lastMessage", "Voice Message", "lastMessageTime", System.currentTimeMillis(), "unreadCounts", newCounts)
            }
        }
    }
}
"""

content = content.replace("}\n", "}\n" + new_methods)

# Wait, replace the LAST "}" is tricky. Let's do it by finding the last occurrence.
last_brace_index = content.rfind("}")
if last_brace_index != -1:
    content = content[:last_brace_index] + new_methods + "\n"

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "w") as f:
    f.write(content)

