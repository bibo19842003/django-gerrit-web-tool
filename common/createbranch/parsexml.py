#!/usr/bin/env python

import xml.dom.minidom
import os
import sys

default_xml = sys.argv[1]
dom = xml.dom.minidom.parse(default_xml)
manifest = dom.documentElement

defaultproject = manifest.getElementsByTagName("default")[0]
defaultrevision = defaultproject.getAttribute("revision")
defaultremote = defaultproject.getAttribute("remote")

projects = manifest.getElementsByTagName("project")
for project in projects:
    name = project.getAttribute("name")

    if project.getAttribute("path"):
        path = project.getAttribute("path")
    else:
        path = name

    if project.getAttribute("revision"):
        newrevision = project.getAttribute("revision")
    else:
        newrevision = defaultrevision

    print "%s:%s" % (name, newrevision)
