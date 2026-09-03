import re

with open("app/src/main/java/com/example/ui/screens/library/LibraryScreen.kt", "r") as f:
    content = f.read()

# Make LibraryScreen load HistoryRepository
import_history = """import com.example.data.repository.HistoryRepository
import com.example.data.repository.LibraryRepository"""
content = content.replace("import com.example.data.repository.LibraryRepository", import_history)

repo_init = """    val libraryRepository = remember { LibraryRepository(context) }
    val downloadRepository = remember { DownloadRepository(context) }"""
new_repo_init = """    val libraryRepository = remember { LibraryRepository(context) }
    val downloadRepository = remember { DownloadRepository(context) }
    val historyRepository = remember { HistoryRepository(context) }
    val historyItems by historyRepository.getHistoryItems().collectAsState(initial = emptyList())"""
content = content.replace(repo_init, new_repo_init)

display_items = """        val displayItems = if (selectedTab == watchlistStr) {
            libraryItems
        } else if (selectedTab == downloadsStr) {
            downloadedItems.map { 
                 com.example.data.model.LibraryItem(
                    id = it.id, 
                    title = it.title, 
                    posterUrl = it.posterUrl, 
                    isMovie = it.isMovie
                ) 
             }
        } else {
            emptyList()
        }"""
new_display_items = """        val displayItems = if (selectedTab == watchlistStr) {
            libraryItems
        } else if (selectedTab == downloadsStr) {
            downloadedItems.map { 
                 com.example.data.model.LibraryItem(
                    id = it.id, 
                    title = it.title, 
                    posterUrl = it.posterUrl, 
                    isMovie = it.isMovie
                ) 
             }
        } else if (selectedTab == stringResource(R.string.history)) {
            historyItems.map { 
                 com.example.data.model.LibraryItem(
                    id = it.id, 
                    title = it.title, 
                    posterUrl = it.posterUrl, 
                    isMovie = it.isMovie
                ) 
             }
        } else {
            emptyList()
        }"""
content = content.replace(display_items, new_display_items)

with open("app/src/main/java/com/example/ui/screens/library/LibraryScreen.kt", "w") as f:
    f.write(content)
