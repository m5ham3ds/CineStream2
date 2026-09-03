import re

with open("app/src/main/java/com/example/ui/screens/social/ChatScreen.kt", "r") as f:
    content = f.read()

old_items = """            items(messages.reversed()) { msg ->
                val isMe = msg.senderId == currentUser?.uid
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 4.dp),
                    horizontalArrangement = if (isMe) Arrangement.End else Arrangement.Start
                ) {
                    Column(
                        horizontalAlignment = if (isMe) Alignment.End else Alignment.Start
                    ) {
                        val isDeletedForMe = msg.deletedFor.contains(currentUser?.uid)
                if (isDeletedForMe) return@items
                
                val isEffectivelyDeleted = msg.isDeleted"""

new_items = """            items(messages.reversed()) { msg ->
                val isMe = msg.senderId == currentUser?.uid
                val isDeletedForMe = msg.deletedFor.contains(currentUser?.uid)
                if (isDeletedForMe) return@items
                
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 4.dp),
                    horizontalArrangement = if (isMe) Arrangement.End else Arrangement.Start
                ) {
                    Column(
                        horizontalAlignment = if (isMe) Alignment.End else Alignment.Start
                    ) {
                        val isEffectivelyDeleted = msg.isDeleted"""

content = content.replace(old_items, new_items)

with open("app/src/main/java/com/example/ui/screens/social/ChatScreen.kt", "w") as f:
    f.write(content)
