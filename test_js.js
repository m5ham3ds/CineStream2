var loc = window.location.href.toLowerCase();
// search clicks
var firstResult = document.querySelector('a.Block--Item, .movieItem a, .anime-card a, .post-item a, .item a, .media-block a, .Blocks-Grid-Item a, .grid-item a, .box a, article a, .result-item a, .title a, h3 a');
if (firstResult && !loc.includes('episode') && !loc.includes('watch')) {
    window.location.href = firstResult.href;
}
