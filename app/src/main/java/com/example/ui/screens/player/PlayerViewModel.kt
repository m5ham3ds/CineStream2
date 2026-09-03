package com.example.ui.screens.player

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.repository.TmdbMediaRepositoryImpl
import com.example.domain.models.Episode
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

data class PlayerUiState(
    val isLoading: Boolean = true,
    val mediaId: String = "",
    val isMovie: Boolean = true,
    val title: String = "",

    // Website (Provider)
    val availableWebsites: List<String> = listOf(
        "VidSrc",
        "SuperStream",
        "FlixHQ",
        "Goku",
        "EgyBest",
        "FaselHD",
        "EgyDead",
        "Anime4Up",
        "WitAnime",
        "CimaLeek",
        "Asia2TV",
        "TukTukCinema",
        "ArabSeedTV",
        "ArabSeedWine",
        "CimaLight",
        "EgyBestLive",
        "StarDima",
        "WatchStarDima"
    ),
    val currentWebsite: String = "VidSrc",

    // Server
    val availableServers: List<String> = emptyList(),
    val currentServer: String = "",

    // Quality
    val availableQualities: List<String> = listOf("Auto", "1080p", "720p"),
    val currentQuality: String = "Auto",

    // Episodes
    val episodes: List<Episode> = emptyList(),
    val currentEpisodeId: String = "",
    val currentSeasonNumber: Int = 1,
    val currentEpisodeNumber: Int = 1,

    // Extracted URL
    val currentVideoUrl: String? = null,
    val extractionUrl: String? = null // The URL to feed to the hidden WebView
)

class PlayerViewModel : ViewModel() {
    private val tmdbRepo = TmdbMediaRepositoryImpl()

    private val _uiState = MutableStateFlow(PlayerUiState())
    val uiState: StateFlow<PlayerUiState> = _uiState.asStateFlow()

    fun initialize(mediaId: String, isMovie: Boolean, initialTitle: String, directUrl: String? = null) {
        val hasArabic = initialTitle.any { it in '\u0600'..'\u06FF' }
        val isAnime = initialTitle.contains("anime", ignoreCase = true) || initialTitle.contains("أنمي", ignoreCase = true)

        val bestWebsite = when {
            hasArabic -> "EgyDead"
            isAnime -> "Anime4Up"
            else -> "VidSrc"
        }

        _uiState.value = _uiState.value.copy(
            mediaId = mediaId,
            isMovie = isMovie,
            title = initialTitle,
            currentWebsite = bestWebsite
        )

        if (!directUrl.isNullOrEmpty()) {
            _uiState.value = _uiState.value.copy(currentVideoUrl = directUrl, isLoading = false)
        } else if (!isMovie) {
            loadEpisodes(mediaId, 1) // Default to season 1
        } else {
            generateExtractionUrl()
        }
    }

    private fun loadEpisodes(seriesId: String, seasonNumber: Int) {
        viewModelScope.launch {
            try {
                // Fetch full series details to get episodes for the season
                val series = tmdbRepo.getSeriesById(seriesId)
                val season = series?.seasons?.find { it.seasonNumber == seasonNumber }
                if (season != null) {
                    val fullSeason = tmdbRepo.getSeasonEpisodes(seriesId, seasonNumber)
                    _uiState.value = _uiState.value.copy(
                        episodes = fullSeason,
                        currentEpisodeId = fullSeason.firstOrNull()?.id ?: "",
                        currentSeasonNumber = seasonNumber,
                        currentEpisodeNumber = fullSeason.firstOrNull()?.episodeNumber ?: 1
                    )
                }
                generateExtractionUrl()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    fun selectWebsite(website: String) {
        _uiState.value = _uiState.value.copy(currentWebsite = website, isLoading = true, currentVideoUrl = null)
        generateExtractionUrl()
    }

    fun selectServer(server: String) {
        _uiState.value = _uiState.value.copy(currentServer = server, isLoading = true, currentVideoUrl = null)
        generateExtractionUrl() // In a real app, this might change the iframe URL params
    }

    fun selectEpisode(episode: Episode) {
        _uiState.value = _uiState.value.copy(
            currentEpisodeId = episode.id,
            currentEpisodeNumber = episode.episodeNumber,
            title = episode.title,
            isLoading = true,
            currentVideoUrl = null
        )
        generateExtractionUrl()
    }

    fun setExtractedUrl(url: String) {
        // Only set if we don't already have one, or if it's a new quality selection
        if (_uiState.value.currentVideoUrl != url) {
            _uiState.value = _uiState.value.copy(
                currentVideoUrl = url,
                isLoading = false
            )
        }
    }

    fun updateServers(servers: List<String>) {
        if (_uiState.value.availableServers != servers && servers.isNotEmpty()) {
            _uiState.value = _uiState.value.copy(
                availableServers = servers,
                currentServer = servers.first()
            )
        }
    }

    private fun generateExtractionUrl() {
        val state = _uiState.value
        val encodedTitle = try {
            java.net.URLEncoder.encode(state.title, "UTF-8")
        } catch (e: Exception) {
            state.title
        }

        val url = if (state.isMovie) {
            when (state.currentWebsite) {
                "VidSrc" -> "https://vidsrc.me/embed/movie?tmdb=${state.mediaId}"
                "SuperStream" -> "https://multiembed.mov/?video_id=${state.mediaId}&tmdb=1"
                "FlixHQ" -> "https://vidsrc.to/embed/movie/${state.mediaId}"
                "Goku" -> "https://vidsrc.cc/v2/embed/movie/${state.mediaId}"
                "EgyBest" -> "https://egydead.icu/?s=$encodedTitle"
                "FaselHD" -> "https://faselhd.club/?s=$encodedTitle"
                "EgyDead" -> "https://egydead.icu/?s=$encodedTitle"
                "Anime4Up" -> "https://anime4up.com/?s=$encodedTitle"
                "WitAnime" -> "https://witanime.com/?search_param=animes&s=$encodedTitle"
                "CimaLeek" -> "https://cimaleek.com/?s=$encodedTitle"
                "Asia2TV" -> "https://asia2tv.cc/?s=$encodedTitle"
                "TukTukCinema" -> "https://tuktukcinema.net/?s=$encodedTitle"
                "ArabSeedTV" -> "https://arabseed-tv.com/?s=$encodedTitle"
                "ArabSeedWine" -> "https://www.arabseed.wine/?s=$encodedTitle"
                "CimaLight" -> "https://e.cimalight.co/search.php?keywords=$encodedTitle"
                "EgyBestLive" -> "https://egybests.live/?s=$encodedTitle"
                "StarDima" -> "https://www.stardima.com/search?query=$encodedTitle"
                "WatchStarDima" -> "https://watch.stardima.com/watch/?s=$encodedTitle"
                else -> "https://vidsrc.me/embed/movie?tmdb=${state.mediaId}"
            }
        } else {
            when (state.currentWebsite) {
                "VidSrc" -> "https://vidsrc.me/embed/tv?tmdb=${state.mediaId}&season=${state.currentSeasonNumber}&episode=${state.currentEpisodeNumber}"
                "SuperStream" -> "https://multiembed.mov/?video_id=${state.mediaId}&tmdb=1&s=${state.currentSeasonNumber}&e=${state.currentEpisodeNumber}"
                "FlixHQ" -> "https://vidsrc.to/embed/tv/${state.mediaId}/${state.currentSeasonNumber}/${state.currentEpisodeNumber}"
                "Goku" -> "https://vidsrc.cc/v2/embed/tv/${state.mediaId}/${state.currentSeasonNumber}/${state.currentEpisodeNumber}"
                "EgyBest" -> "https://egydead.icu/?s=$encodedTitle"
                "FaselHD" -> "https://faselhd.club/?s=$encodedTitle"
                "EgyDead" -> "https://egydead.icu/?s=$encodedTitle"
                "Anime4Up" -> "https://anime4up.com/?s=$encodedTitle"
                "WitAnime" -> "https://witanime.com/?search_param=animes&s=$encodedTitle"
                "CimaLeek" -> "https://cimaleek.com/?s=$encodedTitle"
                "Asia2TV" -> "https://asia2tv.cc/?s=$encodedTitle"
                "TukTukCinema" -> "https://tuktukcinema.net/?s=$encodedTitle"
                "ArabSeedTV" -> "https://arabseed-tv.com/?s=$encodedTitle"
                "ArabSeedWine" -> "https://www.arabseed.wine/?s=$encodedTitle"
                "CimaLight" -> "https://e.cimalight.co/search.php?keywords=$encodedTitle"
                "EgyBestLive" -> "https://egybests.live/?s=$encodedTitle"
                "StarDima" -> "https://www.stardima.com/search?query=$encodedTitle"
                "WatchStarDima" -> "https://watch.stardima.com/watch/?s=$encodedTitle"
                else -> "https://vidsrc.me/embed/tv?tmdb=${state.mediaId}&season=${state.currentSeasonNumber}&episode=${state.currentEpisodeNumber}"
            }
        }

        _uiState.value = _uiState.value.copy(extractionUrl = url, isLoading = true)
    }
}
