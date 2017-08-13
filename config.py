#!/usr/bin/python
import configparser
from pathlib import Path
from exception import Type,TeleException

class Config:
	def __init__(self,config_path='config.ini'):
		self.__config=configparser.ConfigParser()		
		self.__config.read(config_path)

	def getValue(self,section,key):
		return self.__config[section].get(key,fallback=None)