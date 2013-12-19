#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  server.py
#  
#  Copyright 2013 Domen Ipavec <domen.ipavec@z-v.si>

import SimpleHTTPServer
import SocketServer
import handler
import os, sys
from daemon import Daemon

PORT = 80

class jasliceServerDaemon(Daemon):
	def run(self):
		try:
			httpd = SocketServer.TCPServer(("", PORT), handler.Handler)
			print "serving at port", PORT
			httpd.serve_forever()
		except:
			pass

		
if __name__ == "__main__":
	daemon = jasliceServerDaemon('/tmp/jaslice-server-daemon.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "Usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
	
