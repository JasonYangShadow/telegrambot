#!/usr/bin/python
import configparser
import logging
from pathlib import Path
from pprint import pprint

LOGGER=logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

class Config:
	def __init__(self,config_path='config.ini'):
		self.__config=configparser.ConfigParser()		
		try:
			path=Path(config_path)
			self.__config.read(path)
		except FileNotFoundError:
			LOGGER.error('config.ini file not found please set it manually')
			raise
		except:
			LOGGER.error('unknown error')
			raise

	def getValue(self,section,key):
		return self.__config[section].get(key,fallback=None)