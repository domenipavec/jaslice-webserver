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
	
	def __init__(self, cfn):
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
			'fire-light': self.fireLight,
			'nebo-mode': self.neboMode,
			'nebo-speed': self.neboSpeed,
			'nebo-other': self.neboOther,
			'utrinek': self.utrinek,
			'save-defaults': self.saveDefaults
		}

		self.cfn = cfn
			
		self.turnOff(None)
		
	def getState(self):
		return self.state

	def act(self, action, parameters):
		if action not in self.acts:
			print "Action does not exist."
		else:
			return self.acts[action](parameters)
		
	def saveDefaults(self, parameters):
		f = open(self.cfn, "wb")
		pickle.dump(self.state, f)
		f.close()
		
	def loadDefaults(self):
		try:
			f = open(self.cfn, "rb")
			self.state = pickle.load(f)
			f.close()
		except:
			self.state = {}
			self.state['fires'] = [{'address': 0x60, 'power': False, 'speed': 128, 'color': 128, 'light': 255},
				{'address': 0x61, 'power': False, 'speed': 128, 'color': 128, 'light': 255}]
			self.state['nebo'] = {'address': 0x50, 'mode': 0, 'speed': 19, 'other': [0,0,0,0]}
			self.state['neboModes'] = [u'Ugasnjeno', u'Normalno', u'Ozvezdja', u'Enakomerno', u'Utripanje posamezno', u'Utripanje več']
	
	def setDefaults(self):
		# fires
		for fire in self.state['fires']:
			if fire['power']:
				self.bus.write_byte(fire['address'], 1)
			self.bus.write_byte_data(fire['address'], 4, fire['speed'])
			self.bus.write_byte_data(fire['address'], 3, fire['light'])
			self.bus.write_byte_data(fire['address'], 2, fire['color'])
		# nebo
		if self.state['nebo']['mode'] != 0:
			self.bus.write_byte_data(self.state['nebo']['address'], 0, self.state['nebo']['mode'])
		self.bus.write_byte_data(self.state['nebo']['address'], 1, self.state['nebo']['speed'])
		for oid in range(4):
			if self.state['nebo']['other'][oid] != 0:
				self.bus.write_byte_data(self.state['nebo']['address'], 2+oid, self.state['nebo']['other'][oid])
	
	def turnOn(self, parameters):
		if USE_GPIO:
			GPIO.output(POWER_ON_PIN, GPIO.HIGH)
			setDefaults()
		self.state['power'] = True
	
	def turnOff(self, parameters):
		if USE_GPIO:
			GPIO.output(POWER_ON_PIN, GPIO.LOW)
		self.loadDefaults()
		self.state['power'] = False
	
	def fireOn(self, parameters):
		fid = int(parameters['id'][0])
		self.state['fires'][fid]['power'] = True
		if USE_SMBUS:
			self.bus.write_byte(self.state['fires'][fid]['address'], 1)
			self.setDefaults()

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

	def neboMode(self, parameters):
		self.state['nebo']['mode'] = int(parameters['mode'][0])
		if USE_SMBUS:
			self.bus.write_byte_data(self.state['nebo']['address'], 0, self.state['nebo']['mode'])
	
	def neboSpeed(self, parameters):
		self.state['nebo']['speed'] = int(parameters['speed'][0])
		if USE_SMBUS:
			self.bus.write_byte_data(self.state['nebo']['address'], 1, self.state['nebo']['speed'])
	
	def neboOther(self, parameters):
		oid = int(parameters['id'][0])
		self.state['nebo']['other'][oid] = int(parameters['other'][0])
		if USE_SMBUS:
			self.bus.write_byte_data(self.state['nebo']['address'], 2+oid, self.state['nebo']['other'][oid])

	def utrinek(self, parameters):
		if USE_SMBUS:
			self.bus.write_byte(0x40, 0)
