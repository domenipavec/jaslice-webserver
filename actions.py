#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  actions.py
#  
#  Copyright 2013 Domen Ipavec <domen.ipavec@z-v.si>

import pickle

class Jaslice:
	
	def __init__(self):
		try:
			f = open("state.pkl", "rb")
			self.state = pickle.load(f)
			f.close()
		except:
			self.state = {'power': False}
		
	def close(self):
		f = open("state.pkl", "wb")
		pickle.dump(self.state, f)
		f.close()

	def getState(self):
		return self.state

	def act(self, action, parameters):
		return {
			'turn-on': self.turnOn,
			'turn-off': self.turnOff,
			}[action](parameters)
	
	def turnOn(self, parameters):
		self.state['power'] = True
	
	def turnOff(self, parameters):
		self.state['power'] = False
	
