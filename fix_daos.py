import re

with open("app/src/main/java/com/example/data/db/LibraryDao.kt", "r") as f:
    content = f.read()

if "clearAll()" not in content:
    content = content.replace("suspend fun deleteItem(item: LibraryItem)", "suspend fun deleteItem(item: LibraryItem)\n    @Query(\"DELETE FROM library_items\")\n    suspend fun clearAll()")
    with open("app/src/main/java/com/example/data/db/LibraryDao.kt", "w") as f:
        f.write(content)

with open("app/src/main/java/com/example/data/db/HistoryDao.kt", "r") as f:
    content = f.read()

if "clearAll()" not in content:
    content = content.replace("suspend fun clearHistory()", "suspend fun clearHistory()\n    @Query(\"DELETE FROM history_items\")\n    suspend fun clearAll()")
    with open("app/src/main/java/com/example/data/db/HistoryDao.kt", "w") as f:
        f.write(content)
        
with open("app/src/main/java/com/example/data/db/WatchedEpisodeDao.kt", "r") as f:
    content = f.read()

if "clearAll()" not in content:
    content = content.replace("suspend fun deleteById(id: String)", "suspend fun deleteById(id: String)\n    @Query(\"DELETE FROM watched_episodes\")\n    suspend fun clearAll()")
    with open("app/src/main/java/com/example/data/db/WatchedEpisodeDao.kt", "w") as f:
        f.write(content)
        
