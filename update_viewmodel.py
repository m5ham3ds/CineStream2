with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "r") as f:
    content = f.read()

old_movie = """        val url = if (state.isMovie) {
            when (state.currentWebsite) {
                "VidSrc" -> "https://vidsrc.me/embed/movie?tmdb=${state.mediaId}"
                "SuperStream" -> "https://multiembed.mov/?video_id=${state.mediaId}&tmdb=1"
                else -> "https://vidsrc.me/embed/movie?tmdb=${state.mediaId}"
            }
        }"""

new_movie = """        val url = if (state.isMovie) {
            when (state.currentWebsite) {
                "VidSrc" -> "https://vidsrc.me/embed/movie?tmdb=${state.mediaId}"
                "SuperStream" -> "https://multiembed.mov/?video_id=${state.mediaId}&tmdb=1"
                "FlixHQ" -> "https://vidsrc.to/embed/movie/${state.mediaId}"
                "Goku" -> "https://vidsrc.cc/v2/embed/movie/${state.mediaId}"
                "EgyBest" -> "https://egydead.icu/movie/${state.mediaId}"
                "FaselHD" -> "https://faselhd.club/?p=${state.mediaId}"
                else -> "https://vidsrc.me/embed/movie?tmdb=${state.mediaId}"
            }
        }"""

old_tv = """        } else {
            when (state.currentWebsite) {
                "VidSrc" -> "https://vidsrc.me/embed/tv?tmdb=${state.mediaId}&season=${state.currentSeasonNumber}&episode=${state.currentEpisodeNumber}"
                "SuperStream" -> "https://multiembed.mov/?video_id=${state.mediaId}&tmdb=1&s=${state.currentSeasonNumber}&e=${state.currentEpisodeNumber}"
                else -> "https://vidsrc.me/embed/tv?tmdb=${state.mediaId}&season=${state.currentSeasonNumber}&episode=${state.currentEpisodeNumber}"
            }
        }"""

new_tv = """        } else {
            when (state.currentWebsite) {
                "VidSrc" -> "https://vidsrc.me/embed/tv?tmdb=${state.mediaId}&season=${state.currentSeasonNumber}&episode=${state.currentEpisodeNumber}"
                "SuperStream" -> "https://multiembed.mov/?video_id=${state.mediaId}&tmdb=1&s=${state.currentSeasonNumber}&e=${state.currentEpisodeNumber}"
                "FlixHQ" -> "https://vidsrc.to/embed/tv/${state.mediaId}/${state.currentSeasonNumber}/${state.currentEpisodeNumber}"
                "Goku" -> "https://vidsrc.cc/v2/embed/tv/${state.mediaId}/${state.currentSeasonNumber}/${state.currentEpisodeNumber}"
                "EgyBest" -> "https://egydead.icu/episode/${state.mediaId}-season-${state.currentSeasonNumber}-ep-${state.currentEpisodeNumber}"
                "FaselHD" -> "https://faselhd.club/?p=${state.mediaId}&s=${state.currentSeasonNumber}&e=${state.currentEpisodeNumber}"
                else -> "https://vidsrc.me/embed/tv?tmdb=${state.mediaId}&season=${state.currentSeasonNumber}&episode=${state.currentEpisodeNumber}"
            }
        }"""

content = content.replace(old_movie, new_movie)
content = content.replace(old_tv, new_tv)

with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "w") as f:
    f.write(content)
