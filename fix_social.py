with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "r") as f:
    content = f.read()

# Find the first occurrence of `fun editMessage` and truncate there
index = content.find("    fun editMessage(conversationId:")
if index != -1:
    content = content[:index]

# Add a closing brace for the class/object
content += "}\n"

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "w") as f:
    f.write(content)

