import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "r") as f:
    content = f.read()

old_signout = """    fun signOut() {
        repository.auth.signOut()
        viewModelScope.launch { repository.getCurrentUser() }
    }"""
new_signout = """    fun signOut() {
        repository.auth.signOut()
        viewModelScope.launch { 
            com.example.data.sync.CloudSyncManager(com.example.MyApplication.instance).clearLocalData()
            repository.getCurrentUser() 
        }
    }"""
content = content.replace(old_signout, new_signout)

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "w") as f:
    f.write(content)

