#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""

"""
import time
import bz2
import pprint
try:
    from lxml import etree
except ImportError:
    #print u""
    raise ImportError(u"[ERROR] The library 'lxml' is required: http://lxml.de/installation.html or sudo apt-get install python-lxml")

class Osm(object):
    def __init__(self, filename):
        self.filename = filename

    def _classifier(self, _tag,_event,_elem):
        """
        """
        if _tag == "way" and _event == "end":
            _tags = {}
            _nodes = []
            for _i in _elem.getchildren():
                if _i.tag == 'tag':
                    _tags[_i.attrib['k']] = _i.attrib['v']
                elif _i.tag == 'nd':
                    _nodes.append( int(_i.attrib['ref']))
            return ('way',int(_elem.attrib['id'])), _elem.attrib,{'nodes':_nodes,'tags':_tags}

        elif _tag == "node" and _event == "end":
            _tags = {}
            _nodes = []
            for _i in _elem.getchildren():
                if _i.tag == 'tag':
                    _tags[_i.attrib['k']] = _i.attrib['v']
            return ('node',int(_elem.attrib['id'])), _elem.attrib,{'tags' : _tags}

        elif _tag == "relation" and _event == "end":
            _tags = {}
            _members = {}
            for _i in _elem.getchildren():
                if _i.tag == 'tag':
                    _tags[_i.attrib['k']] = _i.attrib['v']
                elif _i.tag == 'member':
                    _members[(_i.attrib['type'],int(_i.attrib['ref']))] = _i.attrib.get('role',None)

            return ('relation',int(_elem.attrib['id'])), _elem.attrib,{'members':_members,'tags':_tags}
        #else:
        #    return  None

    def parse( self ):
        _bz2 = bz2.BZ2File( self.filename , 'r' )
        _context = etree.iterparse( _bz2, 
                                    events=("end","start"), 
                                    encoding = 'utf-8')

        #_current_type = None
        #_current_uid = None
        for _event, _elem in _context:
            _tag = _elem.tag
            yield self._classifier(_tag,_event,_elem) 

            # Cleaning memory
            if _event == "start" and (_tag == "way" or _tag == "node" or _tag == "relation"):
                while _elem.getprevious() is not None:
                    _elem.getprevious().clear()
                    del _elem.getparent()[0]

        yield self._classifier(_tag,_event,_elem) 
        del _elem
        del _context
    
if __name__ == '__main__':
    import sys
    try:
        import argparse
    except ImportError:
        raise ImportError(u"[ERROR] The library 'argparse' is required. Install python2.7 or easy_install argparse.")

    #_filename = 'C:/Home/c08937/downloads/spain.osm.bz2'
    #_filename = '/mnt/floppy/maps/spain.osm.bz2'
    #_filename = 'andorra.osm.bz2'
    _parser = argparse.ArgumentParser( description='Reads .osm.bz2 files.' )

    _parser.add_argument( '--onlynodes', 
                          dest='onlynodes', 
                          action='store_true',
                          default=False,
                          help='Show nodes: id lat lon')

    _parser.add_argument( '--onlyways', 
                          dest='onlyways', 
                          action='store_true',
                          default=False,
                          help='Show ways: id [node1,node2,...]')

    _parser.add_argument( '--onlytags', 
                          dest='onlytags', 
                          action='store_true',
                          default=False,
                          help=u"Show ways: type _ id {'key1': 'value1', ...}")

    _parser.add_argument( 'infile', 
                          nargs='?', 
                          type=argparse.FileType('r'),
                          default=sys.stdin)

    #_parser.add_argument( 'outfile', 
    #                      nargs='?', 
    #                      type=argparse.FileType('w'),
    #                      default=sys.stdout)

    _args = _parser.parse_args()
    _time_ini = time.time()

    # Now all the logic...
    _osm = Osm( _args.infile.name )
    if not (_args.onlyways or _args.onlynodes or _args.onlytags):
        for _elem in _osm.parse():
            if _elem != None:
                print '\n',_elem[0][0], ' _ ', _elem[0][1]
                print pprint.pprint( _elem[1] )
                print pprint.pprint( _elem[2] )
    if _args.onlynodes:
        for _elem in _osm.parse():
            if _elem != None:
                if _elem[0][0] == 'node':
                    print _elem[0][1],_elem[1]['lat'],_elem[1]['lon']
    elif _args.onlyways:
        for _elem in _osm.parse():
            if _elem != None:
                if _elem[0][0] == 'way':
                    print _elem[0][1],_elem[2]['nodes']
    elif _args.onlytags:
        for _elem in _osm.parse():
            if _elem != None:
                print _elem[0][0],'_',_elem[0][1], _elem[2]['tags']

    print time.time() - _time_ini , ' sg'
