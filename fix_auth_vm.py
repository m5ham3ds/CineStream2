import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "r") as f:
    content = f.read()

# We want to add the sync call inside signInWithEmail and signUp, OR just in the auth state listener
# Let's add it to auth state listener which handles app start and sign in
old_init = """        repository.auth.addAuthStateListener { auth ->
            viewModelScope.launch {
                val currentAuth = auth.currentUser
                if (currentAuth != null) {
                    if (repository.currentUserFlow.value == null || repository.currentUserFlow.value?.uid != currentAuth.uid) {
                        repository.getCurrentUser()
                    }
                } else {
                    repository.currentUserFlow.value = null
                }
            }
        }"""
new_init = """        repository.auth.addAuthStateListener { auth ->
            viewModelScope.launch {
                val currentAuth = auth.currentUser
                if (currentAuth != null) {
                    if (repository.currentUserFlow.value == null || repository.currentUserFlow.value?.uid != currentAuth.uid) {
                        repository.getCurrentUser()
                        // Sync data from cloud
                        try {
                            com.example.data.sync.CloudSyncManager(com.example.MyApplication.instance).syncFromCloud(currentAuth.uid)
                        } catch (e: Exception) {
                            e.printStackTrace()
                        }
                    }
                } else {
                    repository.currentUserFlow.value = null
                }
            }
        }"""

content = content.replace(old_init, new_init)

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "w") as f:
    f.write(content)
