# osm2hdf5
Adapted from [BitBucket](https://bitbucket.org/josemaria.alkala/)

Many **GIS applications** are using **NASA HDF5**. At this moment there is no easy to use to use tool to convert from **OpenStreetMap format to NASA HDF5**, so the data from OSM can not be used freely by these applications.

These scripts have been taken from and updated for use with the recent version of PyTables and other dependencies
*[OsmReader](https://bitbucket.org/josemaria.alkala/osmreader)* and
*[Osm2HDF5](https://bitbucket.org/josemaria.alkala/osm2hdf5)*.
The author of the above repositories seems not to be updating them actively

The users of the scripts will be able to do the following

###**1) osmreader.py (Description: Prints all the Nodes, Ways and Tags to stdout)**

**command: `python osmreader.py <infile:type:osm.bz2>`**

**output:**
```
<truncated>
node  _  193620070
{'changeset': '795708', 'uid': '35009', 'timestamp': '2009-03-12T16:45:02Z', 'lon': '76.3670104', 'version': '4', 'user': 'dockers', 'lat': '9.5021492', 'id': '193620070'}
None
{'tags': {}}
None
<truncated>
```

**command: `python osmreader.py --onlytags <infile:type:osm.bz2>`**

[similarly --onlynodes and --only ways can be passed for filteration]

**output (Prints all Tags associated with the Nodes to stdout):**
```
<truncated>
node _ 15850058 {'created_by': 'JOSM'}
node _ 15977516 {}
node _ 16173235 {'is_capital': 'state', 'name:mr': u'\u092e\u0941\u0902\u092c\u0908', 'name:kn': u'\u0cae\u0cc1\u0c82\u0cac\u0cc8', 'name:cs': 'Bombaj', 'rank': '0', 'name:ru': u'\u041c\u0443\u043c\u0431\u0430\u0438', 'name:de': 'Mumbai', 'name:te': u'\u0c2e\u0c41\u0c02\u0c2c\u0c48', 'name:ta': u'\u0bae\u0bc1\u0bae\u0bcd\u0baa\u0bc8', 'is_in:country': 'India', 'wikipedia': 'en:Mumbai', 'ele': '8', 'source': 'http://en.wikipedia.org/wiki/Mumbai', 'name:fr': 'Bombay', 'capital': '4', 'name:sk': 'Bombaj', 'name:hi': u'\u092e\u0941\u0902\u092c\u0908', 'is_in:country_code': 'IN', 'is_in:state': 'Maharashtra', 'name:bn': u'\u09ae\u09c1\u09ae\u09cd\u09ac\u0987', 'name:uk': u'\u041c\u0443\u043c\u0431\u0430\u0457', 'old_name': 'Bombay', 'name:sr': u'\u041c\u0443\u043c\u0431\u0430\u0458', 'population': '13662885', 'name:en': 'Mumbai', 'name:jbo': '.mumbais.', 'name': 'Mumbai', 'place:cca': 'a1', 'place': 'city', 'name:gu': u'\u0aae\u0ac1\u0a82\u0aac\u0a88', 'is_in:continent': 'Asia', 'name:es': 'Bombay'}
<truncated>
```

###**2) osm2hdf5.py (Description: Converts input file of .osm.bz2 to NASA HDF5 format)**

**command: `python osm2hdf5.py <infile:type:osm.bz2> <outfile:type:hdf5|h5>`**
**output: None | Errors (if encountered)**

Benchmark: The script took 41.88 min to convert the following to HDF5 format

india-latest.osm.bz2	2015-06-05 06:24	405500845 bytes
