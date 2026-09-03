package com.example.utils

import android.content.Context
import com.startapp.sdk.adsbase.StartAppAd

object AdManager {
    fun showInterstitial(context: Context) {
        // This static method will show an interstitial ad if one is loaded, 
        // or attempt to load and show it immediately.
        StartAppAd.showAd(context)
    }
}
