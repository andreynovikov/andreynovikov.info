Title: Android action bar tabs with fragments having separate back stack for each tab
Date: 2014-02-21 13:57
Modified: 2014-01-24 13:57
Category: Программирование
Tags:программирование, android
Slug: programming-android-fragments-back-stack

It took me three days to solve the issue of overlapping fragments, lost history and failure to display fragments after device rotation. There are a lot of discussions on these subjects on StackOverflow none of them providing a good working solution. At last I have found a [good answer](http://stackoverflow.com/a/8582894/488489) describing the general approach. I've strictly followed the advice and got the working solution which I want now to share with the rest. I have created a [Gist](https://gist.github.com/4619215) containing all necessary code.
