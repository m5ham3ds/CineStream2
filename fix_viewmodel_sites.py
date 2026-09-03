import re

with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "r") as f:
    content = f.read()

# Replace availableWebsites
old_sites = 'val availableWebsites: List<String> = listOf("VidSrc", "SuperStream", "AutoEmbed")'
new_sites = 'val availableWebsites: List<String> = listOf("VidSrc", "SuperStream", "FlixHQ", "Goku", "EgyBest", "FaselHD")'
content = content.replace(old_sites, new_sites)

# Replace availableServers
old_servers = 'val availableServers: List<String> = listOf("Auto Server 1", "Auto Server 2")'
new_servers = 'val availableServers: List<String> = listOf("Server 1", "Server 2", "VIP Server", "Fast Server")'
content = content.replace(old_servers, new_servers)
content = content.replace('val currentServer: String = "Auto Server 1"', 'val currentServer: String = "Server 1"')

with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "w") as f:
    f.write(content)
