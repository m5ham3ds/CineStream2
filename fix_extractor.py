with open("app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt", "r") as f:
    content = f.read()

# Update function signature
old_sig = """fun HiddenVideoExtractor(
    url: String,
    onVideoUrlFound: (String) -> Unit
) {"""
new_sig = """fun HiddenVideoExtractor(
    url: String,
    isMovie: Boolean = true,
    season: Int = 1,
    episode: Int = 1,
    onVideoUrlFound: (String) -> Unit
) {"""
content = content.replace(old_sig, new_sig)

# Update Javascript injection
old_js = """                        val autoPlayScript = \"\"\"
                            (function() {
                                setInterval(function() {
                                    var iframes = document.getElementsByTagName('iframe');
                                    for (var i = 0; i < iframes.length; i++) {
                                        try {
                                            var playBtn = iframes[i].contentWindow.document.querySelector('.play-button, .jw-icon-display, video');
                                            if (playBtn) playBtn.click();
                                        } catch(e) {}
                                    }
                                    
                                    var localPlay = document.querySelector('.play-button, .jw-icon-display, video');
                                    if (localPlay) localPlay.click();
                                }, 1000);
                            })();
                        \"\"\".trimIndent()"""

new_js = """                        val autoPlayScript = \"\"\"
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
                        \"\"\".trimIndent()"""
content = content.replace(old_js, new_js)

with open("app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt", "w") as f:
    f.write(content)
