import re

with open("app/src/main/java/com/example/ui/screens/profile/EditProfileScreen.kt", "r") as f:
    content = f.read()

imports_to_add = """import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.result.PickVisualMediaRequest
import androidx.compose.foundation.clickable
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import coil.compose.AsyncImage
import com.example.R
import androidx.compose.material.icons.filled.Edit
"""

# Insert imports
content = content.replace("import androidx.compose.runtime.*", "import androidx.compose.runtime.*\n" + imports_to_add)

state_to_add = """    var isProfilePublic by remember(currentUser) { mutableStateOf(currentUser?.isProfilePublic ?: true) }
    var selectedPhotoUri by remember { mutableStateOf<android.net.Uri?>(null) }
    
    val photoPickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.PickVisualMedia()
    ) { uri ->
        if (uri != null) {
            selectedPhotoUri = uri
        }
    }
"""

content = content.replace("    var isProfilePublic by remember(currentUser) { mutableStateOf(currentUser?.isProfilePublic ?: true) }", state_to_add)

photo_ui = """
            // Profile Picture Editor
            Box(
                modifier = Modifier
                    .size(120.dp)
                    .clip(CircleShape)
                    .background(Color.DarkGray)
                    .clickable {
                        photoPickerLauncher.launch(
                            PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)
                        )
                    },
                contentAlignment = Alignment.Center
            ) {
                AsyncImage(
                    model = selectedPhotoUri ?: currentUser?.photoUrl?.takeIf { it.isNotEmpty() } ?: R.drawable.ic_launcher_background,
                    contentDescription = "Profile Picture",
                    modifier = Modifier.fillMaxSize(),
                    contentScale = ContentScale.Crop
                )
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(Color.Black.copy(alpha = 0.4f)),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(Icons.Default.Edit, contentDescription = "Edit Photo", tint = Color.White, modifier = Modifier.size(32.dp))
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
            
            OutlinedTextField(
"""

content = content.replace("            OutlinedTextField(", photo_ui, 1)

update_call = """authViewModel.updateProfile(firstName, lastName, username, isProfilePublic, selectedPhotoUri) { success, error ->"""
content = content.replace("authViewModel.updateProfile(firstName, lastName, username, isProfilePublic, null) { success, error ->", update_call)

with open("app/src/main/java/com/example/ui/screens/profile/EditProfileScreen.kt", "w") as f:
    f.write(content)
