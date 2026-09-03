import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()


old_play_movie = """                    Button(
                        onClick = { 
                            if (downloadItem?.isCompleted == true) {
                                onPlay(movie.title, "local_offline_file://${downloadItem.id}")
                            } else {
                                isDownloadMode = false; showSourceSheet = true 
                            }
                        },"""
new_play_movie = """                    Button(
                        onClick = { 
                            if (downloadItem?.isCompleted == true) {
                                onPlay(movie.title, "local_offline_file://${downloadItem.id}")
                            } else {
                                onPlay(movie.title, "") 
                            }
                        },"""
content = content.replace(old_play_movie, new_play_movie)

old_play_series = """                        Button(
                            onClick = {
                                if (firstUnplayedEpisode != null) {
                                    selectedEpisodeForSource = firstUnplayedEpisode
                                    isDownloadMode = false
                                    showSourceSheet = true
                                } else {
                                    Toast.makeText(context, "No episodes available", Toast.LENGTH_SHORT).show()
                                }
                            },"""
new_play_series = """                        Button(
                            onClick = {
                                if (firstUnplayedEpisode != null) {
                                    onPlay("${series.title} - ${firstUnplayedEpisode.title}", "")
                                } else {
                                    Toast.makeText(context, "No episodes available", Toast.LENGTH_SHORT).show()
                                }
                            },"""
content = content.replace(old_play_series, new_play_series)

# Also EpisodeItem onClick
old_episode_click = """                            modifier = Modifier.clickable { 
                                selectedEpisodeForSource = episode
                                isDownloadMode = false
                                showSourceSheet = true
                            }"""
new_episode_click = """                            modifier = Modifier.clickable { 
                                onPlay("${series.title} - ${episode.title}", "")
                            }"""
content = content.replace(old_episode_click, new_episode_click)


with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
