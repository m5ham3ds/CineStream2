import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

imports = """import com.example.ui.theme.MyApplicationTheme
import com.example.utils.NotificationHelper
import com.startapp.sdk.adsbase.StartAppAd
import com.startapp.sdk.adsbase.StartAppSDK"""

content = content.replace(
    "import com.example.ui.theme.MyApplicationTheme\nimport com.example.utils.NotificationHelper",
    imports
)

init_code = """    super.onCreate(savedInstanceState)
    
    // Initialize Start.io SDK with a placeholder App ID.
    // Replace "YOUR_STARTAPP_APP_ID" with your actual Start.io App ID.
    StartAppSDK.init(this, "YOUR_STARTAPP_APP_ID", false)
    StartAppAd.disableSplash()"""

content = content.replace("    super.onCreate(savedInstanceState)", init_code)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
