with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace('"YOUR_STARTAPP_APP_ID"', '"208324071"')

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
