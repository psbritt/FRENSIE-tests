#! /usr/bin/env python
from xml.etree import ElementTree
from xml.dom import minidom

def prettify(elem, filename):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    xml = reparsed.toprettyxml(indent="  ")

    f = open(filename, 'w')
    f.write( xml[23:] )
