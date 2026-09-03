with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "r") as f:
    content = f.read()

old_sites = 'val availableWebsites: List<String> = listOf("VidSrc", "SuperStream", "FlixHQ", "Goku", "EgyBest", "FaselHD")'
new_sites = 'val availableWebsites: List<String> = listOf("VidSrc", "SuperStream", "FlixHQ", "EgyDead", "FaselHD", "Anime4Up", "WitAnime", "CimaLeek", "Asia2TV", "TukTukCinema")'

content = content.replace(old_sites, new_sites)

# Update the extraction logic to handle some of them gracefully
old_movie_routing = """                "FaselHD" -> "https://faselhd.club/?p=${state.mediaId}"
                else -> "https://vidsrc.me/embed/movie?tmdb=${state.mediaId}"
            }"""
new_movie_routing = """                "FaselHD" -> "https://faselhd.club/?p=${state.mediaId}"
                "EgyDead" -> "https://egydead.icu/movie/${state.mediaId}"
                "Anime4Up" -> "https://anime4up.com/?s=${state.title}" // Uses search
                "WitAnime" -> "https://witanime.com/?search_param=animes&s=${state.title}"
                "CimaLeek" -> "https://cimaleek.com/?s=${state.title}"
                "Asia2TV" -> "https://asia2tv.com/?s=${state.title}"
                "TukTukCinema" -> "https://tuktukcinema.com/?s=${state.title}"
                else -> "https://vidsrc.me/embed/movie?tmdb=${state.mediaId}"
            }"""
content = content.replace(old_movie_routing, new_movie_routing)

old_tv_routing = """                "FaselHD" -> "https://faselhd.club/?p=${state.mediaId}&s=${state.currentSeasonNumber}&e=${state.currentEpisodeNumber}"
                else -> "https://vidsrc.me/embed/tv?tmdb=${state.mediaId}&season=${state.currentSeasonNumber}&episode=${state.currentEpisodeNumber}"
            }"""
new_tv_routing = """                "FaselHD" -> "https://faselhd.club/?p=${state.mediaId}&s=${state.currentSeasonNumber}&e=${state.currentEpisodeNumber}"
                "EgyDead" -> "https://egydead.icu/episode/${state.mediaId}-season-${state.currentSeasonNumber}-ep-${state.currentEpisodeNumber}"
                "Anime4Up" -> "https://anime4up.com/?s=${state.title}" // Will require WebView to click first result
                "WitAnime" -> "https://witanime.com/?search_param=animes&s=${state.title}"
                "CimaLeek" -> "https://cimaleek.com/?s=${state.title}"
                "Asia2TV" -> "https://asia2tv.com/?s=${state.title}"
                "TukTukCinema" -> "https://tuktukcinema.com/?s=${state.title}"
                else -> "https://vidsrc.me/embed/tv?tmdb=${state.mediaId}&season=${state.currentSeasonNumber}&episode=${state.currentEpisodeNumber}"
            }"""
content = content.replace(old_tv_routing, new_tv_routing)


with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "w") as f:
    f.write(content)
