import re

with open("app/src/main/java/com/example/ui/screens/social/ChatScreen.kt", "r") as f:
    content = f.read()

# 1. Add imports
imports = """import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.combinedClickable
import androidx.compose.material.icons.outlined.Mic
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.ContentCopy
import androidx.compose.material.icons.outlined.MicNone
import androidx.compose.material.icons.filled.Block
import androidx.compose.material.icons.filled.PlayArrow
import android.widget.Toast
import androidx.compose.ui.platform.LocalContext
import com.example.data.repository.PrivateMessage
"""

content = content.replace("import androidx.compose.foundation.clickable", "import androidx.compose.foundation.clickable\n" + imports)

# 2. Add ExperimentalFoundationApi if not present
if "@OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class)" not in content:
    content = content.replace("@OptIn(ExperimentalMaterial3Api::class)", "@OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class)")

# 3. Add state for editing and selecting messages
state_add = """    val currentUser by viewModel.currentUser.collectAsState()
    val context = LocalContext.current
    var selectedMessage by remember { mutableStateOf<PrivateMessage?>(null) }
    var editingMessage by remember { mutableStateOf<PrivateMessage?>(null) }
    var showDeleteConfirm by remember { mutableStateOf(false) }
"""
content = content.replace("    val currentUser by viewModel.currentUser.collectAsState()", state_add)

# 4. Remove Search icon
search_icon = 'IconButton(onClick = {}) { Icon(Icons.Default.Search, contentDescription = "Search", tint = primaryRed) }'
content = content.replace(search_icon, "")

# 5. Modify Input area for Edit mode and Mic
bottom_bar_old = """Box(modifier = Modifier.weight(1f)) {
                        if (messageText.isEmpty()) {
                            Text("Type a message...", color = Color.Gray, fontSize = 16.sp)
                        }
                        BasicTextField(
                            value = messageText,
                            onValueChange = { messageText = it },
                            textStyle = TextStyle(color = Color.White, fontSize = 16.sp),
                            cursorBrush = SolidColor(primaryRed),
                            modifier = Modifier.fillMaxWidth()
                        )
                    }
                    
                    Icon(Icons.Default.Face, contentDescription = "Emoji", tint = primaryRed, modifier = Modifier.size(24.dp))
                    
                    Spacer(modifier = Modifier.width(12.dp))
                    
                    Box(
                        modifier = Modifier
                            .size(48.dp)
                            .clip(CircleShape)
                            .background(primaryRed)
                            .clickable {
                                viewModel.sendMessage(messageText)
                                messageText = ""
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.AutoMirrored.Filled.Send, contentDescription = "Send", tint = Color.White)
                    }"""

bottom_bar_new = """Box(modifier = Modifier.weight(1f)) {
                        if (messageText.isEmpty()) {
                            Text(if (editingMessage != null) "Edit message..." else "Type a message...", color = Color.Gray, fontSize = 16.sp)
                        }
                        BasicTextField(
                            value = messageText,
                            onValueChange = { messageText = it },
                            textStyle = TextStyle(color = Color.White, fontSize = 16.sp),
                            cursorBrush = SolidColor(primaryRed),
                            modifier = Modifier.fillMaxWidth()
                        )
                    }
                    
                    Icon(Icons.Default.Face, contentDescription = "Emoji", tint = primaryRed, modifier = Modifier.size(24.dp))
                    
                    Spacer(modifier = Modifier.width(12.dp))
                    
                    Box(
                        modifier = Modifier
                            .size(48.dp)
                            .clip(CircleShape)
                            .background(primaryRed)
                            .clickable {
                                if (messageText.isNotBlank()) {
                                    if (editingMessage != null) {
                                        viewModel.editMessage(editingMessage!!.id, messageText)
                                        editingMessage = null
                                    } else {
                                        viewModel.sendMessage(messageText)
                                    }
                                    messageText = ""
                                } else {
                                    // Send voice message
                                    viewModel.sendVoiceMessage("local_voice_path.m4a")
                                    Toast.makeText(context, "Voice message sent", Toast.LENGTH_SHORT).show()
                                }
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        if (messageText.isNotBlank() || editingMessage != null) {
                            Icon(Icons.AutoMirrored.Filled.Send, contentDescription = "Send", tint = Color.White)
                        } else {
                            Icon(Icons.Outlined.MicNone, contentDescription = "Voice", tint = Color.White)
                        }
                    }"""

content = content.replace(bottom_bar_old, bottom_bar_new)

# 6. Update Message bubble with Long Press and Tombstone
msg_bubble_old = """Box(
                            modifier = Modifier
                                .background(
                                    color = if (isMe) primaryRed else darkGray,
                                    shape = RoundedCornerShape(
                                        topStart = 20.dp,
                                        topEnd = 20.dp,
                                        bottomStart = if (isMe) 20.dp else 4.dp,
                                        bottomEnd = if (isMe) 4.dp else 20.dp
                                    )
                                )
                                .padding(horizontal = 16.dp, vertical = 10.dp)
                        ) {
                            Text(text = msg.text, color = Color.White, fontSize = 15.sp)
                        }"""

msg_bubble_new = """val isDeletedForMe = msg.deletedFor.contains(currentUser?.uid)
                if (isDeletedForMe) return@items
                
                val isEffectivelyDeleted = msg.isDeleted
                
                Box(
                            modifier = Modifier
                                .background(
                                    color = if (isEffectivelyDeleted) Color.Transparent else if (isMe) primaryRed else darkGray,
                                    shape = RoundedCornerShape(
                                        topStart = 20.dp,
                                        topEnd = 20.dp,
                                        bottomStart = if (isMe) 20.dp else 4.dp,
                                        bottomEnd = if (isMe) 4.dp else 20.dp
                                    )
                                )
                                .border(if (isEffectivelyDeleted) 1.dp else 0.dp, if (isEffectivelyDeleted) Color.Gray else Color.Transparent, RoundedCornerShape(20.dp))
                                .combinedClickable(
                                    onClick = {},
                                    onLongClick = {
                                        if (!isEffectivelyDeleted) {
                                            selectedMessage = msg
                                        }
                                    }
                                )
                                .padding(horizontal = 16.dp, vertical = 10.dp)
                        ) {
                            if (isEffectivelyDeleted) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Default.Block, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(16.dp))
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Text(text = "تم حذف هذه الرسالة", color = Color.Gray, fontSize = 14.sp)
                                }
                            } else if (msg.isVoice) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = Color.White, modifier = Modifier.size(24.dp))
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Box(modifier = Modifier.width(100.dp).height(2.dp).background(Color.White.copy(alpha = 0.5f)))
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Text("0:12", color = Color.White, fontSize = 12.sp)
                                }
                            } else {
                                Column {
                                    Text(text = msg.text, color = Color.White, fontSize = 15.sp)
                                    if (msg.isEdited) {
                                        Text(text = "Edited", color = Color.White.copy(alpha = 0.5f), fontSize = 10.sp, modifier = Modifier.align(Alignment.End))
                                    }
                                }
                            }
                        }
                        
                        // Show Reactions if any
                        if (!isEffectivelyDeleted && msg.reactions.isNotEmpty()) {
                            Row(modifier = Modifier.padding(top = 2.dp)) {
                                msg.reactions.values.distinct().forEach { emoji ->
                                    Text(text = emoji, fontSize = 14.sp, modifier = Modifier.background(Color(0xFF2C2C2E), CircleShape).padding(horizontal = 4.dp, vertical = 2.dp))
                                }
                            }
                        }"""

content = content.replace(msg_bubble_old, msg_bubble_new)

# 7. Add Bottom Sheet / Dialog for Actions
bottom_sheet_ui = """
    if (selectedMessage != null) {
        ModalBottomSheet(onDismissRequest = { selectedMessage = null }, containerColor = Color(0xFF1E1E1E)) {
            val msg = selectedMessage!!
            val isMe = msg.senderId == currentUser?.uid
            val isLastMessage = messages.firstOrNull { it.senderId == currentUser?.uid }?.id == msg.id
            
            Column(modifier = Modifier.fillMaxWidth().padding(bottom = 32.dp)) {
                // Reactions
                Row(
                    modifier = Modifier.fillMaxWidth().padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    val emojis = listOf("👍", "❤️", "😂", "😮", "😢", "🙏")
                    emojis.forEach { emoji ->
                        Text(
                            text = emoji,
                            fontSize = 28.sp,
                            modifier = Modifier.clickable {
                                viewModel.reactToMessage(msg.id, emoji)
                                selectedMessage = null
                            }.padding(8.dp)
                        )
                    }
                }
                
                HorizontalDivider(color = Color.DarkGray)
                
                if (!msg.isVoice) {
                    ListItem(
                        headlineContent = { Text("Copy", color = Color.White) },
                        leadingContent = { Icon(Icons.Outlined.ContentCopy, contentDescription = null, tint = Color.White) },
                        colors = ListItemDefaults.colors(containerColor = Color.Transparent),
                        modifier = Modifier.clickable {
                            val clipboard = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager
                            clipboard.setPrimaryClip(android.content.ClipData.newPlainText("message", msg.text))
                            Toast.makeText(context, "Copied", Toast.LENGTH_SHORT).show()
                            selectedMessage = null
                        }
                    )
                }
                
                if (isMe && isLastMessage && !msg.isVoice) {
                    ListItem(
                        headlineContent = { Text("Edit", color = Color.White) },
                        leadingContent = { Icon(Icons.Outlined.Edit, contentDescription = null, tint = Color.White) },
                        colors = ListItemDefaults.colors(containerColor = Color.Transparent),
                        modifier = Modifier.clickable {
                            editingMessage = msg
                            messageText = msg.text
                            selectedMessage = null
                        }
                    )
                }
                
                ListItem(
                    headlineContent = { Text("Delete", color = Color(0xFFE50914)) },
                    leadingContent = { Icon(Icons.Outlined.Delete, contentDescription = null, tint = Color(0xFFE50914)) },
                    colors = ListItemDefaults.colors(containerColor = Color.Transparent),
                    modifier = Modifier.clickable {
                        if (isMe) {
                            showDeleteConfirm = true
                        } else {
                            viewModel.deleteMessage(msg.id, false)
                            selectedMessage = null
                        }
                    }
                )
            }
        }
    }
    
    if (showDeleteConfirm && selectedMessage != null) {
        AlertDialog(
            onDismissRequest = { showDeleteConfirm = false },
            title = { Text("Delete Message", color = Color.White) },
            text = { Text("Who do you want to delete this message for?", color = Color.Gray) },
            confirmButton = {
                TextButton(onClick = {
                    viewModel.deleteMessage(selectedMessage!!.id, true)
                    showDeleteConfirm = false
                    selectedMessage = null
                }) { Text("Delete for Everyone", color = Color(0xFFE50914)) }
            },
            dismissButton = {
                TextButton(onClick = {
                    viewModel.deleteMessage(selectedMessage!!.id, false)
                    showDeleteConfirm = false
                    selectedMessage = null
                }) { Text("Delete for Me", color = Color.White) }
            },
            containerColor = Color(0xFF1E1E1E)
        )
    }
"""

content = content.replace("    } // LazyColumn closing bracket", "    }\n" + bottom_sheet_ui)

# Wait, `} // LazyColumn closing bracket` is not a thing.
# Let's find the end of `ChatScreen` composable properly.
# Insert it right before the last closing brace.

last_brace_index = content.rfind("}")
if last_brace_index != -1:
    content = content[:last_brace_index] + bottom_sheet_ui + "\n}"


with open("app/src/main/java/com/example/ui/screens/social/ChatScreen.kt", "w") as f:
    f.write(content)
