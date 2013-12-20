#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  debug.py
#  
#  Copyright 2013 Domen Ipavec <domen.ipavec@z-v.si>

import SimpleHTTPServer
import SocketServer
import handler
import os, sys

PORT = 80

httpd = SocketServer.TCPServer(("", PORT), handler.Handler)
print "serving at port", PORT
httpd.serve_forever()
