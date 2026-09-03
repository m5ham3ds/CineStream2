package com.example.ui.screens.player

import android.annotation.SuppressLint
import android.os.Handler
import android.os.Looper
import android.webkit.CookieManager
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView

@SuppressLint("SetJavaScriptEnabled")
@Composable
fun HiddenVideoExtractor(
    url: String,
    isMovie: Boolean = true,
    season: Int = 1,
    episode: Int = 1,
    onVideoUrlFound: (String) -> Unit
) {
    AndroidView(
        modifier = Modifier.size(1.dp).alpha(0f), // Completely invisible but active in layout
        factory = { ctx ->
            WebView(ctx).apply {
                setLayerType(android.view.View.LAYER_TYPE_SOFTWARE, null)
                settings.apply {
                    javaScriptEnabled = true
                    domStorageEnabled = true
                    databaseEnabled = true
                    javaScriptCanOpenWindowsAutomatically = true
                    userAgentString = WebSettings.getDefaultUserAgent(ctx)
                    mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
                    cacheMode = WebSettings.LOAD_DEFAULT
                    // This is critical: force media to auto-play so we can catch the network request
                    mediaPlaybackRequiresUserGesture = false 
                }

                val cookieManager = CookieManager.getInstance()
                cookieManager.setAcceptCookie(true)
                cookieManager.setAcceptThirdPartyCookies(this, true)

                webViewClient = object : WebViewClient() {
                    override fun shouldInterceptRequest(
                        view: WebView?,
                        request: WebResourceRequest?
                    ): WebResourceResponse? {
                        val reqUrl = request?.url.toString()
                        
                        // Look for standard streaming formats
                        if (reqUrl.contains(".m3u8") || reqUrl.contains(".mp4")) {
                            // Avoid common ad scripts that might have these strings
                            if (!reqUrl.contains("adsystem") && !reqUrl.contains("tracker")) {
                                Handler(Looper.getMainLooper()).post {
                                    onVideoUrlFound(reqUrl)
                                }
                            }
                        }
                        
                        return super.shouldInterceptRequest(view, request)
                    }

                    override fun onPageFinished(view: WebView, url: String) {
                        super.onPageFinished(view, url)
                        // Inject script to automatically click play buttons to force stream load
                        val autoPlayScript = """
                            (function() {
                                var isMovie = ${isMovie};
                                var epNum = ${episode};
                                var loc = window.location.href.toLowerCase();
                                
                                // 1. Auto-Click Search Results
                                if (loc.includes('?s=') || loc.includes('search')) {
                                    var firstResult = document.querySelector('.movieItem a, .anime-card a, .post-item a, .item a, .media-block a');
                                    if (firstResult) {
                                        window.location.href = firstResult.href;
                                        return;
                                    }
                                }
                                
                                // 2. Auto-Navigate to Episode
                                if (!isMovie && (loc.includes('/anime/') || loc.includes('/series/') || loc.includes('/season/') || document.querySelector('.EpsList, .episodes-lists'))) {
                                    var links = document.querySelectorAll('a');
                                    for(var i=0; i<links.length; i++) {
                                        var txt = links[i].innerText.trim();
                                        if (txt === 'الحلقة ' + epNum || txt === 'حلقه ' + epNum || txt === ''+epNum) {
                                            window.location.href = links[i].href;
                                            return;
                                        }
                                    }
                                    // Fallback: click first episode if exact not found
                                    var firstEp = document.querySelector('.EpsList a, .episodes-lists a, .episodes a');
                                    if (firstEp && !loc.includes('episode')) {
                                        window.location.href = firstEp.href;
                                        return;
                                    }
                                }
                                
                                // 3. Decode AnimeLuxe / Protected Servers
                                var luxeServer = document.querySelector('.server-list a.btn, .serversList li');
                                if (luxeServer && luxeServer.getAttribute('data-url')) {
                                    try {
                                        var decodedUrl = atob(luxeServer.getAttribute('data-url'));
                                        if (decodedUrl && decodedUrl.includes('http')) {
                                            var iframe = document.createElement('iframe');
                                            iframe.src = decodedUrl;
                                            document.body.appendChild(iframe);
                                        }
                                    } catch(e){}
                                }
                                
                                // 4. Auto-Play Players (MegaMax, VidSrc, etc)
                                setInterval(function() {
                                    var iframes = document.getElementsByTagName('iframe');
                                    for (var i = 0; i < iframes.length; i++) {
                                        try {
                                            var playBtn = iframes[i].contentWindow.document.querySelector('.play-button, .jw-icon-display, video, .vjs-big-play-button');
                                            if (playBtn) playBtn.click();
                                        } catch(e) {}
                                    }
                                    var localPlay = document.querySelector('.play-button, .jw-icon-display, video, .vjs-big-play-button');
                                    if (localPlay) localPlay.click();
                                }, 1500);
                            })();
                        """.trimIndent()
                        view.evaluateJavascript(autoPlayScript, null)
                    }
                }
            }
        },
        update = { webView ->
            if (webView.url != url) {
                webView.loadUrl(url)
            }
        }
    )
}
