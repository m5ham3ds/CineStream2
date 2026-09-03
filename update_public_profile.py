import re

with open("app/src/main/java/com/example/ui/screens/profile/PublicProfileScreen.kt", "r") as f:
    content = f.read()

# I need to insert imports
imports = """import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.material.icons.outlined.*
"""
content = content.replace("import androidx.compose.foundation.background", imports + "\nimport androidx.compose.foundation.background")

state_add = """    var selectedStat by remember { mutableStateOf<String?>(null) }
"""
content = content.replace("val surfaceColor = Color(0xFF1C1C1E)", "val surfaceColor = Color(0xFF1C1C1E)\n    val primaryRed = Color(0xFFE50914)\n" + state_add)

# Replacing the Bio part with Stats and content
old_bio = """                    } else { 
                        Surface(
                            shape = RoundedCornerShape(12.dp),
                            color = surfaceColor,
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Column(modifier = Modifier.padding(16.dp)) {
                                Text("Bio", color = Color.Gray, fontSize = 14.sp)
                                Spacer(modifier = Modifier.height(8.dp))
                                Text("Hi, I'm using CineStream!", color = Color.White, fontSize = 16.sp)
                            }
                        }
                    }"""

new_bio = """                    } else {
                        // Subscription Plan
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .border(1.dp, primaryRed.copy(alpha = 0.5f), RoundedCornerShape(12.dp))
                                .background(surfaceColor, RoundedCornerShape(12.dp))
                                .padding(16.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Box(
                                modifier = Modifier.size(40.dp).clip(CircleShape).background(Color(0xFF2C2C2E)),
                                contentAlignment = Alignment.Center
                            ) {
                                Text("👑", fontSize = 20.sp)
                            }
                            Spacer(modifier = Modifier.width(16.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text("Premium Member", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                        
                        Spacer(modifier = Modifier.height(24.dp))
                        
                        // Stats Row
                        Row(
                            modifier = Modifier.fillMaxWidth().background(surfaceColor, RoundedCornerShape(12.dp)).padding(16.dp),
                            horizontalArrangement = Arrangement.SpaceEvenly
                        ) {
                            PublicStatItem(Icons.Outlined.Movie, "24", "Movies", primaryRed) { selectedStat = "Movies" }
                            PublicStatItem(Icons.Outlined.Tv, "12", "Series", primaryRed) { selectedStat = "Series" }
                            PublicStatItem(Icons.Outlined.Face, "5", "Anime", primaryRed) { selectedStat = "Anime" }
                        }
                        
                        Spacer(modifier = Modifier.height(24.dp))
                        
                        if (selectedStat != null) {
                            Text("$selectedStat Activity", color = Color.White, fontSize = 18.sp, fontWeight = FontWeight.Bold, modifier = Modifier.align(Alignment.Start))
                            Spacer(modifier = Modifier.height(16.dp))
                            
                            // Mock Grid
                            LazyVerticalGrid(
                                columns = GridCells.Fixed(3),
                                horizontalArrangement = Arrangement.spacedBy(8.dp),
                                verticalArrangement = Arrangement.spacedBy(8.dp),
                                modifier = Modifier.height(300.dp)
                            ) {
                                items(9) { index ->
                                    Box(modifier = Modifier.aspectRatio(0.7f).clip(RoundedCornerShape(8.dp)).background(Color.DarkGray)) {
                                        AsyncImage(
                                            model = "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dENvU.jpg",
                                            contentDescription = null,
                                            contentScale = ContentScale.Crop,
                                            modifier = Modifier.fillMaxSize()
                                        )
                                    }
                                }
                            }
                        }
                    }"""
content = content.replace(old_bio, new_bio)

helper = """
@Composable
fun PublicStatItem(icon: androidx.compose.ui.graphics.vector.ImageVector, count: String, label: String, tintColor: Color, onClick: () -> Unit) {
    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.clickable { onClick() }.padding(4.dp)) {
        Icon(icon, contentDescription = null, tint = tintColor, modifier = Modifier.size(28.dp))
        Spacer(modifier = Modifier.height(8.dp))
        Text(count, color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(4.dp))
        Text(label, color = Color.Gray, fontSize = 12.sp)
    }
}
"""
content = content + "\n" + helper

with open("app/src/main/java/com/example/ui/screens/profile/PublicProfileScreen.kt", "w") as f:
    f.write(content)

