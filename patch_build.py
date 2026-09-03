import re

with open("app/build.gradle.kts", "r") as f:
    content = f.read()

if "com.startapp:inapp-sdk" not in content:
    content = content.replace(
        "dependencies {",
        "dependencies {\n  implementation(\"com.startapp:inapp-sdk:5.1.0\")"
    )
    with open("app/build.gradle.kts", "w") as f:
        f.write(content)
