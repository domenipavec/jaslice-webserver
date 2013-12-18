#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  handler.py
#  
#  Copyright 2013 Domen Ipavec <domen.ipavec@z-v.si>

import SimpleHTTPServer
import actions
from jinja2 import Environment, FileSystemLoader

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def __init__(self, request, ca, s):
		self.jaslice = actions.Jaslice()
		self.env = Environment(loader=FileSystemLoader('/home/domen/jaslice-webserver/templates'))
		SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, request, ca, s)
	
	def do_GET(self):
		psplit = self.path.split('/')
		if psplit[1] == 'act':
			if len(psplit) > 2:
				print "Action:", psplit[2]
				self.handleAction(psplit[2], psplit[3:])
			
			self.send_response(302, "Action executed")
			if len(self.headers.getheaders('referer')) > 0:
				referer = self.headers.getheaders('referer')[0]
			else:
				referer = "/"
			self.send_header("Location", referer)
		else:
			template = self.env.get_template("index.html")
			self.wfile.write(template.render(self.jaslice.getState()).encode('utf-8'))
		self.jaslice.close()

	def handleAction(self, action, parameters):
		try:
			self.jaslice.act(action, parameters)
		except:
			print "Action does not exist."
