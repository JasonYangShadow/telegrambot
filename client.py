#!/usr/bin/python
import telepot
import logging
import time
from pprint import pprint
from config import Config
from mongo import Mongo
from exception import Type, TeleException

LOGGER=logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

class Client:
	def __init__(self):
		self.__config=Config()
		self.__mongo=Mongo()
		self.__db_msg=self.__config.getValue('Config','DB_MSG')

	def insertMsg(self,user,msg):
		self.__mongo.saveUpdateOne({"chat_user":user},{'$set':{"chat_body":msg}},self.__db_msg)


if __name__ == '__main__':
	client=Client()
	client.insertMsg('jasonyangshadow', 'test oh!!!')