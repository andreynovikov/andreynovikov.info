Title: When OSM is not enough, part 1
Date: 2016-12-21 15:16
Category: Картография
Tags: maptrek, trekarta
Slug: sasplanet-howto
Image: /sasplanet-howto/IMG_0372.JPG
ImagePosition: 40%
Status: published

###The problem

On your trip to Cyprus you might want to see three beautiful medieval bridges: Roudia Bridge, Kelefos Bridge and Elia Bridge.

<!-- PELICAN_END_SUMMARY -->

![]({attach}sasplanet-howto/IMG_0372.JPG){: class="centered" }

The last two can be easily accessed from a good road but the first one is hidden from most of tourists deep in the mountains.
If you are accustomed to off-road driving you can rent a great Suzuki Jimny 4х4 and go for a ride.

![]({attach}sasplanet-howto/DSC_9307.JPG)

But much greater challenge is to drive from Roudia to Kelefos bridge directly through mountains. (Disclaimer: take this ride only
if you are brave and confident enough.)

![]({attach}sasplanet-howto/DSC_9456.JPG)

For the later task using OSM map along may be not enough: satellite map can become very handy in some situations. (During my
trip via this route I two times came to the situation when the road was blocked - one time by a fence, second time by a landslide.)

That's why I want to show you how to prepare custom offline maps for Trekarta from online sources. This is where a very handy
SAS.Planet application comes into place.

###Solution

Download SAS.Planet application from [http://www.sasgis.org/download/](http://www.sasgis.org/download/). It does not have
an installer so you just have to unpack it to a folder of your choice. Run SAS.Planet. If you run it for the first time
you can appreciate the number of supported maps in corresponding menu.

First you have to decide which area you need. For our case I have prepared a [GPX file]({attach}sasplanet-howto/Cyprus Bridges.gpx) with bridge points. Open it in application:

![]({attach}sasplanet-howto/01.png){: class="centered" }

Then select a map of your choice. This is _ArcGIS Imagery_ in our case:

![]({attach}sasplanet-howto/02.png){: class="centered" }

You can see how nicely all roads are visible on the imagery. Having that in your mobile device will let you select and drive
roads that are not present on OSM map.

Using selection menu select the area you want to create a map for:

![]({attach}sasplanet-howto/03.png){: class="centered" }

In our case it covers mountain area between two bridges. The third bridge is accessible by good road from the second one, so
we won't extend map area there:

![]({attach}sasplanet-howto/04.png){: class="centered" }

After you finish Selection Manager will open. Before you will be able to create a map you need to download all the tiles
for selected area. First check that correct map is selected as source (you can view one map but download another in fact).
Then select zoom levels you want to download. In our case the source does not have zooms bigger then 18 and there is no
much sense to view imagery in zooms smaller than 15. Take into account resulting number of tiles. When everything looks
good start the download:

![]({attach}sasplanet-howto/05.png){: class="centered" }

Depending on the number of tiles and map source productivity it can take from minutes to hours:

![]({attach}sasplanet-howto/06.png){: class="centered" }

When download is finished press Selection Manager button (in the bottom left corner) or, if you have occasionally closed
this window, use selection menu to open last selection. Go to Export tab. First select MBTiles format. Then select the same
zoom levels as you have used for download. Recheck that correct map is selected. Optionally give descriptive name to a map.
Finally select the output file:

![]({attach}sasplanet-howto/07.png){: class="centered" }

After export is finished transfer resulting file to device (it should have .mbtiles extension). Open file manager on
device and tap the file. File open dialog should appear if you do this for the first time. Select _Trekarta data import_:

![]({attach}sasplanet-howto/08.png){: class="centered" }

Trekarta will import the map to the internal folder (you can remove the source file after that):

![]({attach}sasplanet-howto/09.png){: class="centered" }

Open Trekarta and tap _Maps_ button:

![]({attach}sasplanet-howto/10.png){: class="centered" }

Select the map you have just created and appreciate the result:

![]({attach}sasplanet-howto/11.png){: class="centered" }

You can see that it covers native OSM map, so you can play with transparency slider if you wish.

![]({attach}sasplanet-howto/12.png){: class="centered" }

###Conclusion

SAS.Planet application is very powerful. Take time to explore its features to get maximum from it. You can create many
map files and use them in Trekarta on demand. In fact MBTiles is popular format used by many other map applications, so
once created you can use the same map in any application of your choice, not only in Trekarta.

[Next time]({filename}maptiler-howto.md) I will show you how to create a map from single image with a help of another great application.
