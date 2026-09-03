with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

old_cond = """                        if (!currentRoute.contains("movie_details") && !currentRoute.contains("series_details")) {"""
new_cond = """                        if (!currentRoute.contains("movie_details") && !currentRoute.contains("series_details") && !currentRoute.contains("player") && !currentRoute.contains("trailer")) {"""
content = content.replace(old_cond, new_cond)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
