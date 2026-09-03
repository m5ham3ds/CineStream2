package com.example.ui.components

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DownloadQualitySheet(
    onDismiss: () -> Unit,
    onQualitySelected: (String) -> Unit
) {
    val qualities = listOf(
        "1080p (FHD)", 
        "720p (HD)", 
        "480p (SD)"
    )

    ModalBottomSheet(onDismissRequest = onDismiss) {
        Column(
            modifier = Modifier
                .padding(16.dp)
                .fillMaxWidth()
        ) {
            Text(
                text = "Select Download Quality", 
                style = MaterialTheme.typography.titleLarge, 
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(bottom = 16.dp)
            )
            
            qualities.forEach { quality ->
                TextButton(
                    onClick = { 
                        onQualitySelected(quality)
                        onDismiss()
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 4.dp),
                    contentPadding = PaddingValues(vertical = 16.dp)
                ) {
                    Text(text = quality, fontSize = 18.sp)
                }
            }
            Spacer(modifier = Modifier.height(32.dp))
        }
    }
}
