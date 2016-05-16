Title: MapTrek - second alpha coming
Date: 2016-05-16 15:36
Category: Картография
Tags: maptrek
Slug: maptrek-second-alpha

Development of [MapTrek](http://maptrek.mobi/) is going in full steam. The following is done in less then a month:

1. __Maps download from application.__ I consider downloading and copying maps by hand not acceptable in 21th century. Despite the fact that this is a temporary solution, because I more and more think that default MapsForge maps are bad, I have implemented maps downloading from within application. If you zoom a map to the 8th level or more and no map for that area is present application will advice to download a suitable map file. Maps are taken from public MapsForge repository and it has one major disadvantage - repository does not cover the whole world, some countries are missing. Personally I find OpenAndroMaps more appealing but their policy forbids automatic downloading. Maps are downloaded by built-in Android download manager, so it is fail safe for connectivity problems. As soon as the map file is downloaded it is made available for MapTrek. No application reload is required.

2. __Enhanced track recording.__ After some experiments I threw away idea of using open file formats for storing internal data. They are text based, very "heavy" and unmanageable. For instance 12 hour track took minutes to write and to read. If there was a need to just change its color, I had to completely rewrite 4MB file. I have created my own binary format, now it takes _2 seconds_ to write 12 hour track, file is tree times smaller and any changes to track properties are instant. Of course I will later add ability to export them to open file formats.

3. __Data management is almost finished.__ I have added support for external GPX/KML files. Currently they have to be manually put in _data_ folder, but later I will add import from external sources. There are no management capabilities, but all data can be seen on the map and used in navigation. I have added ability to edit description and color of waypoints, but amendments are currently saved only to internal database. Left are track details view and ability to save amendments to external sources. There will be also possibility to move waypoints from/to external sources.

4. __Some map rendering enhancements.__ I am working on some map rendering enhancements in background, but I do not have much time to spend on that. Also I lack some knowledge in that area, so I takes more time than I want.

I hope to get to orientation change support shortly. It means not only smartphone rotation but also a proper support for tablets. Stay tuned!

![]({attach}maptrek-second-alpha.png){: class="centered" }
