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
    onVideoUrlFound: (String) -> Unit,
    onServersFound: ((List<String>) -> Unit)? = null
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

                addJavascriptInterface(object {
                    @android.webkit.JavascriptInterface
                    fun sendServers(serversStr: String) {
                        val servers = serversStr.split(",").filter { it.isNotBlank() }
                        if (servers.isNotEmpty()) {
                            Handler(Looper.getMainLooper()).post {
                                onServersFound?.invoke(servers)
                            }
                        }
                    }
                }, "AndroidBridge")

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
                                    var firstResult = document.querySelector('.Block--Item, .movieItem a, .anime-card a, .post-item a, .item a, .media-block a, .Blocks-Grid-Item a, .grid-item a, .box a, article a, .result-item a, h3 a, .post a, .thumb a, .title a, .box-item a, .video-item a, .poster a');
                                    if (firstResult && !loc.includes('episode') && !loc.includes('watch')) {
                                        window.location.href = firstResult.href;
                                        return;
                                    }
                                }
                                
                                // 2. Auto-Navigate to Episode (for Series/Anime)
                                if (!isMovie) {
                                    var links = document.querySelectorAll('a');
                                    for(var i=0; i<links.length; i++) {
                                        var txt = links[i].innerText.trim();
                                        if (txt === 'الحلقة ' + epNum || txt === 'حلقه ' + epNum || txt === ''+epNum || txt === 'Episode ' + epNum) {
                                            window.location.href = links[i].href;
                                            return;
                                        }
                                    }
                                    // Fallback: click first episode if exact not found and we are on a season/series page
                                    if (!loc.includes('episode') && !loc.includes('ep-')) {
                                        var firstEp = document.querySelector('.EpsList a, .episodes-lists a, .episodes a, .episode-link');
                                        if (firstEp) {
                                            window.location.href = firstEp.href;
                                            return;
                                        }
                                    }
                                }
                                
                                // 3. Auto-Play Players (MegaMax, VidSrc, etc)
                                setInterval(function() {
                                    var iframes = document.getElementsByTagName('iframe');
                                    for (var i = 0; i < iframes.length; i++) {
                                        try {
                                            var playBtn = iframes[i].contentWindow.document.querySelector('.play-button, .jw-icon-display, video, .vjs-big-play-button');
                                            if (playBtn) playBtn.click();
                                            // Also click the iframe itself if possible
                                        } catch(e) {}
                                    }
                                    var localPlay = document.querySelector('.play-button, .jw-icon-display, video, .vjs-big-play-button');
                                    if (localPlay) localPlay.click();
                                    
                                    // Some sites need us to click a watch button first
                                    var watchBtn = document.querySelector('.watch-btn, #watch-btn, a.watch, .btn-watch');
                                    if(watchBtn && !loc.includes('watch')) watchBtn.click();
                                    
                                    // Some sites use servers list to load iframe
                                    var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li');
                                    var serverBtn = document.querySelector('ul.servers li, .server-list li');
                                    if(serverBtn && document.getElementsByTagName('iframe').length === 0) serverBtn.click();
                                    
                                    // Send servers back to Kotlin
                                    if (serverList && serverList.length > 0 && typeof AndroidBridge !== 'undefined') {
                                        var serverNames = [];
                                        for(var i=0; i<serverList.length; i++) {
                                            serverNames.push(serverList[i].innerText.trim());
                                        }
                                        AndroidBridge.sendServers(serverNames.join(','));
                                    }
                                    
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
