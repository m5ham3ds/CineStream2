with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    lines = f.readlines()

in_series = False
for i, line in enumerate(lines):
    if "composable(Screen.SeriesDetails.route)" in line:
        in_series = True
    if in_series and "player?mediaId=$movieId&isMovie=true" in line:
        lines[i] = line.replace("player?mediaId=$movieId&isMovie=true", "player?mediaId=$seriesId&isMovie=false")
        in_series = False

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.writelines(lines)
