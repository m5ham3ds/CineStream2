package com.example.ui.components

import android.app.Activity
import androidx.compose.material3.MaterialTheme
import android.content.Context
import android.content.ContextWrapper
import android.content.pm.ActivityInfo
import android.view.View
import android.view.ViewGroup
import android.widget.FrameLayout
import androidx.activity.compose.BackHandler
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.lifecycle.compose.LocalLifecycleOwner
import androidx.compose.ui.viewinterop.AndroidView
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.pierfrancescosoffritti.androidyoutubeplayer.core.player.YouTubePlayer
import com.pierfrancescosoffritti.androidyoutubeplayer.core.player.listeners.AbstractYouTubePlayerListener
import com.pierfrancescosoffritti.androidyoutubeplayer.core.player.listeners.FullscreenListener
import com.pierfrancescosoffritti.androidyoutubeplayer.core.player.options.IFramePlayerOptions
import com.pierfrancescosoffritti.androidyoutubeplayer.core.player.views.YouTubePlayerView

fun Context.findActivity(): Activity? = when (this) {
    is Activity -> this
    is ContextWrapper -> baseContext.findActivity()
    else -> null
}

@Composable
fun InlineYouTubePlayer(
    videoId: String,
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current
    val lifecycleOwner = LocalLifecycleOwner.current

    var fullScreenView by remember { mutableStateOf<View?>(null) }
    var isFullScreen by remember { mutableStateOf(false) }
    var exitFullscreenAction by remember { mutableStateOf<(() -> Unit)?>(null) }

    BackHandler(enabled = isFullScreen) {
        exitFullscreenAction?.invoke()
    }

    Box(modifier = modifier) {
        AndroidView(
            modifier = Modifier.fillMaxSize(),
            factory = { ctx ->
                val view = YouTubePlayerView(ctx).apply {
                    enableAutomaticInitialization = false
                }
                lifecycleOwner.lifecycle.addObserver(view)

                view.addFullscreenListener(object : FullscreenListener {
                    override fun onEnterFullscreen(fullscreenView: View, exitFullscreen: () -> Unit) {
                        isFullScreen = true
                        fullScreenView = fullscreenView
                        exitFullscreenAction = exitFullscreen
                        ctx.findActivity()?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
                    }
                    override fun onExitFullscreen() {
                        isFullScreen = false
                        fullScreenView = null
                        exitFullscreenAction = null
                        ctx.findActivity()?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
                    }
                })

                val listener = object : AbstractYouTubePlayerListener() {
                    override fun onReady(player: YouTubePlayer) {
                        player.loadVideo(videoId, 0f)
                    }
                }
                
                val options = IFramePlayerOptions.Builder()
                    .controls(1)
                    .fullscreen(1)
                    .build()
                    
                view.initialize(listener, options)
                view
            },
            onRelease = {
                it.release()
            }
        )
    }

    if (isFullScreen && fullScreenView != null) {
        Dialog(
            onDismissRequest = { 
                exitFullscreenAction?.invoke()
            },
            properties = DialogProperties(
                usePlatformDefaultWidth = false,
                decorFitsSystemWindows = false
            )
        ) {
            Box(modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)) {
                AndroidView(
                    modifier = Modifier.fillMaxSize(),
                    factory = { ctx ->
                        FrameLayout(ctx).apply {
                            val parent = fullScreenView?.parent as? ViewGroup
                            parent?.removeView(fullScreenView)
                            addView(fullScreenView)
                        }
                    },
                    onRelease = {
                        val parent = fullScreenView?.parent as? ViewGroup
                        parent?.removeView(fullScreenView)
                    }
                )
            }
        }
    }
}
