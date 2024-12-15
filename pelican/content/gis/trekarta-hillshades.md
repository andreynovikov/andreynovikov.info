Title: Hillshades
Date: 2017-11-29 12:52
Category: Картография
Tags: maptrek, trekarta
Slug: trekarta-hillshades

When I decided to develop Trekarta I didn't plan to implement hillshades as its maps are vector but hillshades are raster.
Later, when I was traveling for the first time with my app through mountains and what-it-looked-like one hour trip
took four hours I have understood that I should add contours visualization.

<!-- PELICAN_END_SUMMARY -->

Next time I went to mountains it looked good but still without hillshades map sometimes was not very descriptive. That's
why when I decided to implement activity modes I undoubtedly wanted to add hillshades to my maps.

Let's look at the examples. First one is a mountain pass I've spent four hours on. Yes, it looks like mountain pass
but visualization is not descriptive at all. Also confusing was that the road was colored as primary road. Contours
are of a little help. But with hillshades enabled you immediatelly see that the path would not be easy one.

![]({attach}trekarta-hillshades1.png){: class="centered" }

Second one is a nice trail to a nearby glacier. It looks smooth and easy but with contours added you understand that
your assumption is not correct. And with hillshades the difficulty of your undertaking can be seen at a glimpse.

![]({attach}trekarta-hillshades2.png){: class="centered" }

And the last example is famous mount Olympus. There are so many paths to take but which one is better? Turning on
contours gives us the clue on the most difficult ones. With hillshades it becomes obvious which paths are steep and which
are gentle. (New hiking mode will visualize it even better.)

![]({attach}trekarta-hillshades3.png){: class="centered" }

I have separated hillshades from native files for two reasons. First, maps are updated weekly while hillshades will
hardly ever update (unless there would appear some new much more detailed source). Second, hillshades are not always
useful. On flat terrains they just add noise and undesired darkening. That's why you can decide to download hillshades
per area. Once been downloaded it does not re-download when you update the area map. As with contours hillshades can be
switched on and off on demand.

I want to express my gratitude to Yves Cainaud from [OpenSnowMap.org](http://opensnowmap.org/) for his crucial help
in provision of crude hillshades for post-processing.
