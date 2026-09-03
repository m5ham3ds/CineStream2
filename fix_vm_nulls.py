with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "r") as f:
    content = f.read()

old_load = """                val series = tmdbRepo.getSeriesById(seriesId)
                val season = series.seasons.find { it.seasonNumber == seasonNumber }"""
new_load = """                val series = tmdbRepo.getSeriesById(seriesId)
                val season = series?.seasons?.find { it.seasonNumber == seasonNumber }"""
content = content.replace(old_load, new_load)

with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "w") as f:
    f.write(content)
