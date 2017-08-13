#!/usr/bin/python
import configparser
from pathlib import Path
from exception import Type,TeleException

LOGGER=logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

class Config:
	def __init__(self,config_path='config.ini'):
		self.__config=configparser.ConfigParser()		
		path=Path(config_path)
		self.__config.read(path)

	def getValue(self,section,key):
		return self.__config[section].get(key,fallback=None)