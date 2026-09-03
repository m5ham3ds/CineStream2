with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "r") as f:
    content = f.read()

models = """
data class PrivateMessage(
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
)

data class Conversation(
    val id: String = "",
    val participants: List<String> = emptyList(),
    val participantNames: Map<String, String> = emptyMap(),
    val lastMessage: String = "",
    val lastMessageTime: Long = 0L,
    val unreadCounts: Map<String, Int> = emptyMap(),
    val isGroup: Boolean = false,
    val isRequest: Boolean = false
)

data class Story(
    val id: String = "",
    val userId: String = "",
    val imageUrl: String = "",
    val timestamp: Long = System.currentTimeMillis()
)

class SocialRepository {
    private val auth = FirebaseAuth.getInstance()
    private val db = FirebaseFirestore.getInstance()

    fun getCurrentUser(): UserProfile? {
        val user = auth.currentUser ?: return null
        return UserProfile(uid = user.uid)
    }

    suspend fun getUserProfile(uid: String): UserProfile? {
        return try {
            val doc = db.collection("users").document(uid).get().await()
            doc.toObject(UserProfile::class.java)
        } catch (e: Exception) {
            null
        }
    }

    fun getStories(): Flow<List<Story>> = callbackFlow {
        val listener = db.collection("stories")
            .orderBy("timestamp", Query.Direction.DESCENDING)
            .addSnapshotListener { snapshot, _ ->
                if (snapshot != null) {
                    val stories = snapshot.toObjects(Story::class.java)
                    trySend(stories)
                }
            }
        awaitClose { listener.remove() }
    }

    fun getConversations(): Flow<List<Conversation>> = callbackFlow {
        val user = auth.currentUser
        if (user == null) {
            trySend(emptyList())
            close()
            return@callbackFlow
        }
        val listener = db.collection("conversations")
            .whereArrayContains("participants", user.uid)
            .orderBy("lastMessageTime", Query.Direction.DESCENDING)
            .addSnapshotListener { snapshot, _ ->
                if (snapshot != null) {
                    val convs = snapshot.toObjects(Conversation::class.java)
                    trySend(convs)
                }
            }
        awaitClose { listener.remove() }
    }

    suspend fun getConversation(conversationId: String): Conversation? {
        return try {
            val doc = db.collection("conversations").document(conversationId).get().await()
            doc.toObject(Conversation::class.java)
        } catch (e: Exception) {
            null
        }
    }

    fun getMessages(conversationId: String): Flow<List<PrivateMessage>> = callbackFlow {
        val listener = db.collection("conversations").document(conversationId)
            .collection("messages")
            .orderBy("timestamp", Query.Direction.ASCENDING)
            .addSnapshotListener { snapshot, _ ->
                if (snapshot != null) {
                    val msgs = snapshot.toObjects(PrivateMessage::class.java)
                    trySend(msgs)
                }
            }
        awaitClose { listener.remove() }
    }

    fun markConversationAsRead(conversationId: String) {
        val user = auth.currentUser ?: return
        val docRef = db.collection("conversations").document(conversationId)
        db.runTransaction { transaction ->
            val snapshot = transaction.get(docRef)
            if (snapshot.exists()) {
                val currentCountsAny = snapshot.get("unreadCounts")
                val currentCounts = if (currentCountsAny is Map<*, *>) {
                    currentCountsAny.entries.associate { it.key.toString() to (it.value.toString().toIntOrNull() ?: 0) }
                } else emptyMap()
                
                val newCounts = currentCounts.toMutableMap()
                newCounts[user.uid] = 0
                transaction.update(docRef, "unreadCounts", newCounts)
            }
        }
    }

    suspend fun createOrGetConversation(otherUserId: String, otherUserName: String): String {
        val user = getCurrentUser() ?: return ""
        val dbUserDoc = db.collection("users").document(user.uid).get().await()
        val realUser = dbUserDoc.toObject(UserProfile::class.java) ?: user
        val participants = listOf(user.uid, otherUserId).sorted()
        val convId = participants.joinToString("_")
        
        val docRef = db.collection("conversations").document(convId)
        val doc = docRef.get().await()
        
        if (!doc.exists()) {
            val conv = Conversation(
                id = convId,
                participants = participants,
                participantNames = mapOf(user.uid to realUser.displayName, otherUserId to otherUserName)
            )
            docRef.set(conv).await()
        }
        return convId
    }

    fun sendMessage(conversationId: String, text: String) {
        val user = getCurrentUser() ?: return
        val docRef = db.collection("conversations").document(conversationId)
        
        val msgRef = docRef.collection("messages").document()
        val msg = PrivateMessage(msgRef.id, user.uid, text, System.currentTimeMillis())
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
                
                transaction.update(docRef, "lastMessage", text, "lastMessageTime", System.currentTimeMillis(), "unreadCounts", newCounts)
            }
        }
    }

    suspend fun searchUsers(query: String): List<UserProfile> {
        return try {
            val snapshot = db.collection("users")
                .whereGreaterThanOrEqualTo("username", query)
                .whereLessThanOrEqualTo("username", query + "\\uf8ff")
                .get()
                .await()
            val result = snapshot.toObjects(UserProfile::class.java)
            result.filter { it.uid != auth.currentUser?.uid }
        } catch (e: Exception) {
            emptyList()
        }
    }
"""

index = content.find("}")
# This is the end of UserProfile
if index != -1:
    content = content[:index+1] + "\n" + models + "\n}\n"

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "w") as f:
    f.write(content)

