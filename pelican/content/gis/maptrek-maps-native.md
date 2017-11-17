Title: Native maps
Date: 2017-11-17 16:13
Category: Картография
Tags: maptrek
Slug: maptrek-maps-native

It took me more then a year to think up, prototype and develop proprietary format for MapTrek maps.
Two times I came to the halt and had to start from the very beginning but finally it was done.
I know that proprietary formats are bad but mapsforge format that I was using is proprietary as well
and has many limits I wanted to eliminate.

<!-- PELICAN_END_SUMMARY -->

At the beginning I wanted to make many before/after screenshots but when new maps were finally ready
I was so tied that I managed to create only one pair:

![]({attach}maptrek-maps-native.png){: class="centered" }

Forest is one of the most representative elements. On the first screen you can see how it is scratched
and over-detailed. The next screen shows the transition from old format to another (upper area is loaded
but lower one remains in old format). The last screen is rendered using only new native maps - forest
is simplified and smoothed.

This is only one of many problems I have solved with new maps format. The benefits of the new format are:

1. Geometry simplification on lower zooms makes map look more legible. It removes many artifacts and fixes rendering errors.

2. Original OSM data is filtered in such way that maps contain only renderable data. This not only saves disk space but also makes areas be downloadable only if they contain visible data.

3. Some data is preprocessed in special way letting me better visualize it or provide extra context.

4. Data in map files can now be used not only for rendering. I have already implemented amenity filtering by their kind and full text search. Soon will come special activity modes for hiking, cycling, skiing and more. I also plan to make map features responsive - so that they can be touched to get extended information. Search for nearby amenities is also in my plans.

5. Map data is now stored in one database file. This let me significantly simplify application logic and improved joint rendering of base and detailed maps.

6. New map creator made it possible to generate most popular tiles first. Now the more popular area is the more fresh data it contains. Generation speed has also significantly increased.

Are there any drawbacks? Of course! I have made lot's of optimizations but still new maps are 30-50% larger then old ones. But I consider this a good tradeoff for so many gainings.


