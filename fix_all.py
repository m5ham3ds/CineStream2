with open("app/src/main/java/com/example/ui/screens/social/ChatScreen.kt", "r") as f:
    content = f.read()

if "import androidx.compose.foundation.border" not in content:
    content = content.replace("import androidx.compose.foundation.background", "import androidx.compose.foundation.background\nimport androidx.compose.foundation.border")

with open("app/src/main/java/com/example/ui/screens/social/ChatScreen.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "r") as f:
    repo_content = f.read()

repo_content = repo_content.replace(
"""    suspend fun searchUsers(query: String): List<UserProfile> {
        return try {
            val snapshot = db.collection("users")
                .whereGreaterThanOrEqualTo("username", query)
                .whereLessThanOrEqualTo("username", query + "\\\\uf8ff")
                .get()
                .await()
            val result = snapshot.toObjects(UserProfile::class.java)
            result.filter { it.uid != auth.currentUser?.uid }
        } catch (e: Exception) {
            emptyList()
        }
    }""",
"""    fun searchUsers(query: String): Flow<List<UserProfile>> = callbackFlow {
        if (query.isBlank()) {
            trySend(emptyList())
            return@callbackFlow
        }
        val listener = db.collection("users")
            .whereGreaterThanOrEqualTo("username", query)
            .whereLessThanOrEqualTo("username", query + "\\uf8ff")
            .addSnapshotListener { snapshot, _ ->
                if (snapshot != null) {
                    val result = snapshot.toObjects(UserProfile::class.java)
                    trySend(result.filter { it.uid != auth.currentUser?.uid })
                }
            }
        awaitClose { listener?.remove() }
    }

    suspend fun saveUserProfile() {
        val user = auth.currentUser ?: return
        val profile = UserProfile(uid = user.uid, username = user.displayName ?: "User", photoUrl = user.photoUrl?.toString() ?: "")
        db.collection("users").document(user.uid).set(profile).await()
    }

    suspend fun startConversation(otherUserId: String, otherUserName: String): String {
        return createOrGetConversation(otherUserId, otherUserName)
    }

    suspend fun addStory(imageUrl: String) {
        val user = auth.currentUser ?: return
        val story = Story(id = "", userId = user.uid, imageUrl = imageUrl, timestamp = System.currentTimeMillis())
        val ref = db.collection("stories").document()
        ref.set(story.copy(id = ref.id)).await()
    }
""")

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "w") as f:
    f.write(repo_content)
