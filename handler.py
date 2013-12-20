#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  handler.py
#  
#  Copyright 2013 Domen Ipavec <domen.ipavec@z-v.si>

import SimpleHTTPServer
import os.path, urlparse
import actions
from jinja2 import Environment, FileSystemLoader

jaslice = actions.Jaslice()

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def __init__(self, request, ca, s):
		paths = ['/home/domen/jaslice-webserver/templates', '/home/domen/github/jaslice-webserver/templates']
		for path in paths:
			if os.path.exists(path):
				self.env = Environment(loader=FileSystemLoader(path))
				break
		SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, request, ca, s)
	
	def do_GET(self):
		url = urlparse.urlparse(self.path)
		psplit = url.path.split('/')
		if psplit[1] == 'act':
			if len(psplit) > 2:
				print "Action:", psplit[2]
				self.handleAction(psplit[2],
					urlparse.parse_qs(url.query)
					)
			self.send_response(302, "Action executed")
			if len(self.headers.getheaders('referer')) > 0:
				referer = self.headers.getheaders('referer')[0]
			else:
				referer = "/"
			self.send_header("Location", referer)
		else:
			template = self.env.get_template("index.html")
			self.wfile.write(template.render(jaslice.getState()).encode('utf-8'))

	def handleAction(self, action, parameters):
		try:
			jaslice.act(action, parameters)
		except:
			print "Action does not exist."
