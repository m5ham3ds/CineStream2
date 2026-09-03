with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "r") as f:
    content = f.read()

content = content.replace("tmdbRepo.getSeriesDetails(seriesId)", "tmdbRepo.getSeriesById(seriesId)")
content = content.replace("tmdbRepo.getSeasonDetails(seriesId, seasonNumber)", "tmdbRepo.getSeasonEpisodes(seriesId, seasonNumber)")

with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "w") as f:
    f.write(content)
