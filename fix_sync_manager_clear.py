import re

with open("app/src/main/java/com/example/data/sync/CloudSyncManager.kt", "r") as f:
    content = f.read()

new_clear_method = """
    suspend fun clearLocalData() {
        db.libraryDao().clearAll()
        db.historyDao().clearAll()
        db.watchedEpisodeDao().clearAll()
    }
}"""
content = content.replace("\n}", new_clear_method)

with open("app/src/main/java/com/example/data/sync/CloudSyncManager.kt", "w") as f:
    f.write(content)
