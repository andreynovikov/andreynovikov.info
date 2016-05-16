Title: Installing and configuring PostGIS
Date: 2015-12-15 18:20
Modified: 2015-12-15 18:20
Category: Картография
Tags: GIS, OSM
Slug: postgis-configuration
Summary: 
Status: draft

```
    sudo apt-get install postgresql
    sudo apt-get install postgis
    sudo -u postgres createuser -s $USER
    createdb gis
    psql -d gis -c 'CREATE EXTENSION hstore; CREATE EXTENSION postgis;'

    sudo apt-get install osm2pgsql
    osm2pgsql --create --slim --cache 4096 --cache-strategy sparse \
	    --number-processes 2 --hstore \
	    --style Workspace/mapzen/vector-datasource/osm2pgsql.style \
		--multi-geometry planet-151207.osm.pbf

    osm2pgsql --create --slim --disable-parallel-indexing --cache 6000 \
        --hstore --hstore-match-only --flat-nodes osm_flat_nodes.bin \
	    --style Workspace/mapzen/vector-datasource/osm2pgsql.style \
		--multi-geometry planet-151207.osm.pbf
```

<http://gis.19327.n5.nabble.com/disk-size-for-planet-osm-import-into-PostGIS-on-an-SSD-td5767230.html>
<http://gis.stackexchange.com/questions/6080/optimizing-osm2pgsql-imports-for-osm-data>
