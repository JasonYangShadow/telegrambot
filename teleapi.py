#!/usr/bin/python
import telepot
import logging
import time
from telepot.loop import MessageLoop
from pprint import pprint
from config import Config
from mongo import Mongo
from exception import Type, TeleException

LOGGER=logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

class Telegram:
	def __init__(self):
		self.__config=Config()
		self.__TOKEN=self.__config.getValue('Telegram','TOKEN')
		if self.__TOKEN is None:
			raise TeleException(Type.NoneException,'TOKEN is none')
		self.__bot=telepot.Bot(self.__TOKEN)
		self.__id=self.__bot.getMe()['id']
		self.__user=self.__bot.getMe()['username']
		self.__mongo=Mongo()
		self.messageProcessing()

	def getBot(self):
		return self.__bot

	def getId(self):
		return self.__id

	def getUserName(self):
		return self.__user

	def messageProcessing(self):
		def handle(msg):
			msg_chat_id=msg['chat']['id']
			msg_username=msg['chat']['username']
			msg_body=msg['text']
			msg_date=msg['date']
			msg_type=msg['chat']['type']
			self.__mongo.saveUpdateOne({'_id':msg_username},{'$set':{'chat_id':msg_chat_id,'chat_type':msg_type,'chat_date':msg_date}})
		MessageLoop(self.__bot,handle).run_as_thread()

	def sendTextMessage(self,username,msg):
		user_list=self.__mongo.find({'_id':username})
		if user_list.size() == 0:
			raise TeleException(Type.NoneException,'No such user!'+username)
		else:
			self.__bot.sendMessage(user_list[0]['chat_id'],msg)

if __name__=="__main__":
	try:
		telebot=Telegram()
		while True:
			time.sleep(5)
	except TeleException as te:
		LOGGER.error(str(te))