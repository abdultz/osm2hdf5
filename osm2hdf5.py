#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""

"""
import time
#import numpy as np
try:
    import tables
except ImportError:
    raise ImportError( u"[ERROR] It is required to install 'pytables': http://www.pytables.org/downloads.html" )

try:
    from osmreader import Osm
except ImportError:
    raise ImportError( u"[ERROR] Download 'osmreader.py' from: https://github.com/abdultz/osm2hdf5/osmreader.py" )
   

class Node( tables.IsDescription ):
    uid  = tables.UInt32Col()
    lat  = tables.Float32Col()
    lon  = tables.Float32Col()
    version = tables.UInt8Col()
    changeset = tables.UInt32Col()
    user_id = tables.UInt32Col()
    visible = tables.BoolCol()
    timestamp = tables.StringCol(20)
    #tables.Time32Atom
    #tables.Time64Atom

class Way( tables.IsDescription ):
    uid  = tables.UInt32Col()
    version = tables.UInt8Col()
    changeset = tables.UInt32Col()
    user_id = tables.UInt32Col()
    visible = tables.BoolCol()
    timestamp = tables.StringCol(20)
    #nds = tables.UInt32Col(shape= (2000,))

class Nd( tables.IsDescription ):
    uid = tables.UInt32Col()
    ref = tables.UInt32Col()

class Relation(tables.IsDescription ):
    uid  = tables.UInt32Col()
    version = tables.UInt8Col()
    changeset = tables.UInt32Col()
    user_id = tables.UInt32Col()
    visible = tables.BoolCol()  # Not sure if it exists.
    timestamp = tables.StringCol(20)
    nds = tables.UInt32Col(shape= (2000,))

class Member( tables.IsDescription ):
    uid = tables.UInt32Col()
    ref_type= tables.StringCol(10)
    ref=  tables.UInt32Col()
    role =  tables.StringCol(100)

class User( tables.IsDescription ):
    uid = tables.UInt32Col()
    username = tables.StringCol(100)

class Tag( tables.IsDescription ):
    uid = tables.UInt32Col()
    kind = tables.StringCol(10)
    key = tables.StringCol(256)
    value = tables.StringCol(256)

class Nodes:
    def __init__(self):
        self.uid = []   #np.array([],dtype= np.uint64 )
        self.lats = []  #np.array([],dtype= np.float32 )
        self.lons = []  #np.array([],dtype= np.float32 )

    def add(self, i, lat, lon):
        self.uid.append( int(i) ) #=  #np.append( self.uid, int(i) )
        self.lats.append( float(lat) )# = #np.append( self.lats, float(lat) )
        self.lons.append( float(lon) ) #np.append( self.lons, float(lon) )

#===============================================    
if __name__ == '__main__':
    import sys
    try:
        import argparse
    except ImportError:
        raise ImportError(u"[ERROR] The library 'argparse' is required. Install python2.7 or easy_install argparse.")

    _parser = argparse.ArgumentParser( description='Converts .osm.bz2 into .h5 file.' )

    _parser.add_argument( 'infile', 
                          nargs='?', 
                          type=argparse.FileType('r'),
                          default=sys.stdin)

    _parser.add_argument( 'outfile', 
                          nargs='?', 
                          type=argparse.FileType('w'),
                          default=sys.stdout)
 
    _args = _parser.parse_args()
    
    # Start timing.
    _time_ini = time.time()

    _osm = Osm( _args.infile.name )

    # H5 creation
    _filter = tables.Filters( complevel=9, 
                              complib='bzip2', 
                              shuffle=True, 
                              fletcher32=False)

    _h5 = tables.openFile( _args.outfile.name,mode='w', filters = _filter)
    _group = _h5.createGroup( _h5.root,"original")
    _h5nodes = _h5.createTable( _group, 'nodes', Node, "Original node data" , filters= _filter)
    _h5tags = _h5.createTable( _group, 'tags', Tag, "Original tags" , filters= _filter)

    _h5ways = _h5.createTable( _group, 'ways', Way, "Original ways data" , filters= _filter)
    _h5nds = _h5.createTable( _group, 'ways_nds', Nd, "Original ways data" , filters= _filter)

    _h5relation = _h5.createTable( _group, 'relations', Way, "Original relation data" , filters= _filter)
    _h5relation_members = _h5.createTable( _group, 'relation_members', Member, "Original relation data" , filters= _filter)
  
    _h5users = _h5.createTable( _group, 'users', User, "Original node data" , filters= _filter)



    _user_dict = {}

    _n = 0
    _m = 0
    for _i in _osm.parse():
        if _i != None:
            _id = _i[0][1]
            _type = _i[0][0]
            _attrib = _i[1]
            _dict = _i[2]
            _uid = int(_attrib.get('uid',0))
            _user = _attrib.get('user',"__nobody__")
            _user_dict[_uid] = _user
            if _type == 'node':
                # Tags
                for _k,_v in _dict['tags'].iteritems():
                    _mytag = _h5tags.row
                    _mytag['uid'] = _id
                    _mytag['kind'] = _type
                    _mytag['key'] = _k.encode('utf-8')
                    _mytag['value'] = _v.encode('utf-8')
                    _mytag.append()                        
                # Attributes
                _n += 1
                _m += 1
                _mynode = _h5nodes.row
                _mynode['uid'] = _id
                _mynode['lat'] = float(_attrib['lat'])
                _mynode['lon'] = float(_attrib['lon'])
                _mynode['version'] = int(_attrib['version'])
                _mynode['changeset'] = int(_attrib['changeset'])
                _mynode['user_id'] = int(_attrib.get('uid',0))
                _mynode['visible'] = bool(_attrib.get('visible', True))
                _mynode['timestamp'] = _attrib['timestamp']
                _mynode.append()

            elif _type == 'way':
                _n += 1
                _m += 1
                _myway = _h5ways.row
                _myway['uid'] = _id
                _myway['version'] = int( _attrib["version"])
                _myway['changeset'] = int( _attrib["changeset"])
                #print _attrib
                _myway['user_id'] = int(_attrib.get('uid',0))
                _myway['visible'] = bool(_attrib.get("visible", True))
                _myway['timestamp'] = _attrib.get("timestamp","")
                _myway.append()

                # Nodes
                for _node in _dict['nodes'].__iter__():
                    _mynd = _h5nds.row
                    _mynd['uid'] = _id
                    _mynd['ref'] = _node
                    _mynd.append()                        
                
                # Tags
                for _k,_v in _dict['tags'].iteritems():
                    _mytag = _h5tags.row
                    _mytag['uid'] = _id
                    _mytag['kind'] = _type
                    _mytag['key'] = _k.encode('utf-8')
                    _mytag['value'] = _v.encode('utf-8')
                    _mytag.append()                        

               
#*                #_users[_uid] = _user
                
            elif _type == 'relation':
                _n += 1
                _m += 1

                # Relation
                _myrelation = _h5relation.row
                _myrelation['uid'] = _id
                _myrelation['version'] = int(_attrib["version"] )
                _myrelation['changeset'] = int( _attrib["changeset"] )
                _myrelation['user_id'] = int(_attrib.get("uid", 0))
                _myrelation['visible'] = bool( _attrib.get("visible", True) )
                _myrelation['timestamp'] = _attrib.get("timestamp",None)

                _myrelation.append()
                # Member
                for _member in _dict['members']:
                    _mymember = _h5relation_members.row
                    _mymember['uid'] = _id
                    _mymember['ref_type'] = _member[0]
                    _mymember['ref'] = _member[1]
                    try:
                        _mymember['role'] = _member[2].encode('utf-8')
                    except:
                        pass
                    _mymember.append()                        
                # Tags
                for _k,_v in _dict['tags'].iteritems():
                    _mytag = _h5tags.row
                    _mytag['uid'] = _id
                    _mytag['kind'] = _type
                    _mytag['key'] = _k.encode('utf-8')
                    _mytag['value'] = _v.encode('utf-8')
                    _mytag.append()                        

                #_user = _attrib.get("user","anonymous")
    
        if _n == 100000:
            print 'Processed: ',_m
            _n=0

    _user = _h5users.row
    for _uid,_name in _user_dict.iteritems():
        _user['uid'] = _uid
        _user['username'] = _name.encode('utf-8')
        _user.append()

    print ( time.time() - _time_ini)/60, ' min'

    _h5.flush()
    _h5.close()
