#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  actions.py
#  
#  Copyright 2013 Domen Ipavec <domen.ipavec@z-v.si>

import pickle
import RPi.GPIO as GPIO
import smbus

POWER_ON_PIN = 12

class Jaslice:
	
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(POWER_ON_PIN, GPIO.OUT)

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
		self.state['fires'] = [{'address': 60, 'power': False, 'speed': 128, 'color': 128, 'light': 255},
			{'address': 61, 'power': False, 'speed': 128, 'color': 128, 'light': 255}]
		self.turnOff(None)
		
	def getState(self):
		return self.state

	def act(self, action, parameters):
		return self.acts[action](parameters)
	
	def turnOn(self, parameters):
		GPIO.output(POWER_ON_PIN, GPIO.HIGH)
		self.state['power'] = True
	
	def turnOff(self, parameters):
		GPIO.output(POWER_ON_PIN, GPIO.LOW)
		self.state['power'] = False
	
	def fireOn(self, parameters):
		self.state['fires'][int(parameters[0])]['power'] = True

	def fireOff(self, parameters):
		self.state['fires'][int(parameters[0])]['power'] = False

	def fireSpeed(self, parameters):
		pass

	def fireLight(self, parameters):
		pass

	def fireColor(self, parameters):
		pass
