Title: User friendly double back exit
Date: 2013-02-11 00:08
Modified: 2016-04-01 14:42
Category: Программирование
Tags: android
Slug: programming-android-double-back
Lang: en
Translation: no

This is the common Android UI pattern to use double Back press to confirm exit from application. It has simple implementation. However there is one thing developers do not think about: when user presses Back the toast with confirmation message is continuing to be displayed after application is already quit.

<!-- PELICAN_END_SUMMARY -->

Here is the solution to this issue:

    :::java
    private Toast backToast;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Create toast in advance
        backToast = Toast.makeText(this, "Press Back again to quit", Toast.LENGTH_SHORT);
        secondBack = false;
    }

    final Handler backHandler = new Handler();
 
    @Override
    public void onBackPressed() {
        if (secondBack) {
            // Cancel the toast to make it stop showing
            backToast.cancel();
            finish();
        } else {
            // Be ready for the second Back
            secondBack = true;
            // Show toast
            backToast.show();
            // Initiate timeout
            backHandler.postDelayed(new Runnable() {
                @Override
                public void run() {
                    secondBack = false;
                }
            }, 2000); // Toast.LENGTH_SHORT lasts for 2000 ms
        }
    }
