Title: Lets talk about maps
Date: 2016-08-19 13:17
Category: Картография
Tags: maptrek, trekarta
Slug: trekarta-maps

Country maps are rectangular. Even if a country is round the map will be rectangular. Yes, it will be visually clipped by country boundary and will look like a circle but it will be stored and processed by application as a rectangle. It does not harm when you operate one map at a time, but if you want to combine several adjacent maps it's a pain. There is no proper way to find out if the map does not contain data because it is clipped or just because there is no data for that area. That's why you have to harvest all maps around. It requires all of them to be opened and consumes extra resources. That's why I decided to go very different way - use square maps.

Nowadays tiled maps have become standard de'facto. That's why Trekarta uses them. The great benefit of tiles is that they have definite size and position. This makes it very easy to position a map and to combine different maps. Maps in Androzic required a lot of computation and still couldn't be combined without visual artifacts. Tiled maps in Trekarta are very easy to operate. This saves both memory resources and battery.

Tiled maps have predefined zoom levels, most commonly from 0 to 20. [Trekarta](https://trekarta.info/) operates from zoom level 2. Each tile has coordinates: X and Y. This makes it easy to address specific tile, just mention zoom, x and y. If you will ever complain about map rendering problem, I will not ask you geographical coordinates, I will better ask you on what tile you see the problem.

Trekarta contains built-in base map that covers whole ([Mercator](https://en.wikipedia.org/wiki/Mercator_projection)) world from zoom level 2 to zoom level 7 (I will explain this choice below). Map is further divided in 128x128 7th-zoom-level parts that can be individually downloaded from server within application. This lets you easily manage maps for your areas of interest making optimal use of storage. For the time-being maps are in well known MapsForge format but are optimized in such way that they are not usable in other applications supporting that format.

![]({attach}trekarta-maps.png){: class="centered" }

Lets return back to the 7th level. It was selected for several reasons:

1. Up to 7th level map contains only overview information that rarely changes. Thus it can be safely embedded in application and not require frequent updates.
2. 2-to-7 zoom world map has acceptable file size, if it would contain 8th level it would be much bigger. This would make application too "heavy".
3. 7th zoom tiles have reasonable area coverage. They provide good compromise between land area and file size.

Unfortunately this setup requires dedicated map server which costs money. But after Mapsforge project refused to accept my contribution of Georgia map (where I plan to travel in a week) I have decided to spend some. It took me tree months to overcome all technical obstacles to generation of square maps. Now when the most of the maps are generated I am very satisfied with the work undertaken.

Unlike country-based maps Trekarta maps cover all the world. If a given square contains _any_ data then a map is available for download. In future I plan to make it more clear - a map will be generated only if it contains _visible_ data. Currently all world maps occupy 42G, modern devices can easily hold them all, which can not be said about application. So, please, download them only on demand.

As a bonus I have improved custom maps support - they can now be semi-transparent and not hide map labels and buildings. This is great for hillshades and other not all-sufficient maps.

By the way, it's very cool that alpha version was downloaded 1817 times and even 10 people have paid for it, but where's the feedback?! I have created a [Q&A Google Group](https://groups.google.com/d/forum/trekarta) for your questions and feedback.
