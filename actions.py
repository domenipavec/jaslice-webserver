#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  actions.py
#  
#  Copyright 2013 Domen Ipavec <domen.ipavec@z-v.si>

import pickle
try:
	import RPi.GPIO as GPIO
	USE_GPIO = True
except:
	print "Could not load GPIO, disabling..."
	USE_GPIO = False
try:
	import smbus
	USE_SMBUS = True
except:
	print "Could not load smbus, disabling..."
	USE_SMBUS = False

POWER_ON_PIN = 12

class Jaslice:
	
	def __init__(self):
		if USE_GPIO:
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(POWER_ON_PIN, GPIO.OUT)

		if USE_SMBUS:
			self.bus = smbus.SMBus(1)

		self.acts = {
			'turn-on': self.turnOn,
			'turn-off': self.turnOff,
			'fire-on': self.fireOn,
			'fire-off': self.fireOff,
			'fire-speed': self.fireSpeed,
			'fire-color': self.fireColor,
			'fire-light': self.fireLight
		}

		self.state = {}
		self.state['fires'] = [{'address': 0x60, 'power': False, 'speed': 128, 'color': 128, 'light': 255},
			{'address': 0x61, 'power': False, 'speed': 128, 'color': 128, 'light': 255}]
		self.turnOff(None)
		
	def getState(self):
		return self.state

	def act(self, action, parameters):
		return self.acts[action](parameters)
	
	def turnOn(self, parameters):
		if USE_GPIO:
			GPIO.output(POWER_ON_PIN, GPIO.HIGH)
		self.state['power'] = True
	
	def turnOff(self, parameters):
		if USE_GPIO:
			GPIO.output(POWER_ON_PIN, GPIO.LOW)
		self.state['power'] = False
	
	def fireOn(self, parameters):
		fid = int(parameters['id'][0])
		self.state['fires'][fid]['power'] = True
		if USE_SMBUS:
			self.bus.write_byte(self.state['fires'][fid]['address'], 1)

	def fireOff(self, parameters):
		fid = int(parameters['id'][0])
		self.state['fires'][fid]['power'] = False
		if USE_SMBUS:
			self.bus.write_byte(self.state['fires'][fid]['address'], 0)

	def fireSpeed(self, parameters):
		fid = int(parameters['id'][0])
		self.state['fires'][fid]['speed'] = int(parameters['speed'][0])
		if USE_SMBUS:
			self.bus.write_byte_data(self.state['fires'][fid]['address'], 4, self.state['fires'][fid]['speed'])

	def fireLight(self, parameters):
		fid = int(parameters['id'][0])
		self.state['fires'][fid]['light'] = int(parameters['light'][0])
		if USE_SMBUS:
			self.bus.write_byte_data(self.state['fires'][fid]['address'], 3, self.state['fires'][fid]['light'])

	def fireColor(self, parameters):
		fid = int(parameters['id'][0])
		self.state['fires'][fid]['color'] = int(parameters['color'][0])
		if USE_SMBUS:
			self.bus.write_byte_data(self.state['fires'][fid]['address'], 2, self.state['fires'][fid]['color'])
