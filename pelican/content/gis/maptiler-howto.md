Title: When OSM is not enough, part 2
Date: 2016-12-22 16:56
Category: Картография
Tags: maptrek, trekarta
Slug: maptiler-howto
Image: /maptiler-howto/00.jpg
Status: published

###Why?

There are situations when a map comes as a one large graphic file. It can be an old-time scanned map, or a software generated water reservoir depth map, or downloaded map of a nature reserve park. Even in this case there are options to import such map in Trekarta. All you need is find a tool that will convert it to MBTiles format. And today I will show you how to do this by creating a usable map from scanned old-time map of Moscow dating back to the year of 1852.

<!-- PELICAN_END_SUMMARY -->

![]({attach}maptiler-howto/00.jpg){: class="centered" }

###How?

My favorite and very powerful tool is MapTiler by Klokan Technologies. It is designed to work under both Windows and Mac OS. It can be downloaded and used for free from [www.maptiler.com](https://www.maptiler.com/) but free version has some limitations that I will describe later.

After installation run MapTiler. Select _Standard Tiles_ and press _Continue_:

![]({attach}maptiler-howto/01.png){: class="centered" }

Select target map image and continue:

![]({attach}maptiler-howto/02.png){: class="centered" }

Select coordinate system of the map. This is a complicated topic and is out of this article scope. Sometimes it can be found on map, sometimes guessed (if you know what all these coordinate systems are), sometimes it can be found in reference file (e.g. OziExplorer calibration file). I will use basic mercator projection for my map:

![]({attach}maptiler-howto/03.png){: class="centered" }

The first thing you have to do is to define geographic location of a map. There are plenty of options for that:

![]({attach}maptiler-howto/04.png){: class="centered" }

I will use georeferencing as I have a simple scanned image without any geographic data in it. Georeferencing is the process of assigning geographical coordinates to specific points of a map. It is required to have at least two reference points located diagonally (unexpectedly MapTiler requires three points), but it is better to have a point for each map corner and even better to ad a point for a map center. In fact you can add as much points as you wish to make matching as precise as possible.

It is easy to define such points if map contains grid lines, but if not you will have to match significant landmarks. In our case it will be historic buildings. In other cases it could be road crossings, river turns, and other distinguishable elements.

![]({attach}maptiler-howto/05.png){: class="centered" }

Georeferencing old map is a bit of challenge because they can not be 100% precise. So it is better to reference as much points as possible. As I will show later MapTiler lets you nicely evaluate the quality of matching. It is always better to start from the center of map. For that you have to find the corresponding area on the reference map and put the marker on the first reference point:

![]({attach}maptiler-howto/06.png){: class="centered" }

Then put the marker on the corresponding object on the target map. You can adjust its position by dragging the magnifier. When finished press the drag anchor and the point will be created. You can press it later to adjust its position:

![]({attach}maptiler-howto/07.png){: class="centered" }

Repeat this as many times as you can. Observe how target map is adjusted while you add more points. As soon as you will define three reference points MapTiler will let you overlay the maps to evaluate the matching (use transparency slider or shift key to look at reference map):

![]({attach}maptiler-howto/08.png){: class="centered" }

I have put 18 points but still could not get nice results, as you can see some points have noticeable offset:

![]({attach}maptiler-howto/09.png){: class="centered" }

If target map is not precise you can play with transformation setting, in my case TPS made a great difference:

![]({attach}maptiler-howto/10.png){: class="centered" }

If target map is not rectangular you can optionally clip the map, this will remove redundant overlapping of underlying map:

![]({attach}maptiler-howto/11.png){: class="centered" }

When finished press _Save_ button. If everything is set press _Continue_ to save the map:

![]({attach}maptiler-howto/12.png){: class="centered" }

To be able to open the map in Trekarta select MBTiles as destination format:

![]({attach}maptiler-howto/13.png){: class="centered" }

Press _Render_ and select destination file. The map will be generated to file. Next steps are as usual: transfer file to device and import it to Trekarta. The procedure is described in detail in [previous article]({filename}sasplanet-howto.md). After that you will be able to appreciate the result:

![]({attach}maptiler-howto/14.png){: class="centered" }

You can see how nicely my scooter track lies on an old-time map!

###Really?

Unfortunately MapTiler is not truly free software. It lets you create a map for free but has two major limitations: it does not let you specify zoom levels you need limiting you with not so good 15th level and it adds watermarks on map tiles. But if you like it and you are not the Unix guru to do all the same in a command line it's worth to be paid for.
