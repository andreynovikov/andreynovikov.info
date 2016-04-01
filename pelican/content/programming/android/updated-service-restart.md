Title: Restarting service after application update in Android
Date: 2012-11-20 10:58
Modified: 2016-04-01 14:42
Category: Программирование
Tags: android
Slug: programming-android-updated-service-restart
Lang: en
Translation: no

If your application is designed as a background service updating it can be a pain because running application is killed during the update. Fortunately your application can request to receive package update broadcast in AndroidManifest.xml (I have added boot completed broadcast here to show that the logic is pretty much the same):

<!-- PELICAN_END_SUMMARY -->

    :::xml
    <receiver android:name=".Starter">
        <intent-filter>
            <action android:name="android.intent.action.BOOT_COMPLETED" />
        </intent-filter>
        <intent-filter>
            <action android:name="android.intent.action.PACKAGE_REPLACED" />
            <data android:scheme="package" />
        </intent-filter>
    </receiver>

Please note that without ```<data .../>``` filter you will not receive a broadcast (do not know why). Also note that many sources state that you can filter by your package name here but it's untrue — package name goes in scheme-specific part of URI but there is no such option in ```<data>``` filter.

Next goes the Starter class:

    :::java
    package your.package;

    import android.content.BroadcastReceiver;
    import android.content.Context;
    import android.content.Intent;
    import android.content.SharedPreferences;
    import android.preference.PreferenceManager;

    public class Starter extends BroadcastReceiver {
        @Override
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(context);
            boolean enabled = prefs.getBoolean("enabled", false);
            if (Intent.ACTION_PACKAGE_REPLACED.equals(action)) {
                enabled &= "your.package".equals(intent.getData().getSchemeSpecificPart());
            }
            if (Intent.ACTION_BOOT_COMPLETED.equals(action)) {
                boolean startAtBoot = prefs.getBoolean("startatboot", false);
                enabled &= startAtBoot;
            }
            if (enabled)
                context.startService(new Intent(context, YourService.class));
        }
    }

Here we do three things:

1. First we check if our service is enabled at all (I assume that application has an option to disable this service).
2. Then if it was a package replaced action we check if this was our package that was updated.
3. Otherwise if it was a boot completed action we check if our application is configured to start at boot (again I assume that application has such option).

That's all, now your background service will be restarted after application update and optionally started after boot.

There is also another question that often goes together with this one: how to start a service after application is installed. The quick answer is: noway. There is no way to receive package installation broadcast by installed application, so your application has to be directly started by user at least once.
