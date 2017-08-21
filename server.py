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

class Server:
	def __init__(self):
		self.__config=Config()
		self.__TOKEN=self.__config.getValue('Telegram','TOKEN')
		if self.__TOKEN is None:
			raise TeleException(Type.NoneException,'TOKEN is none')
		self.__bot=telepot.Bot(self.__TOKEN)
		self.__id=self.__bot.getMe()['id']
		self.__user=self.__bot.getMe()['username']
		self.__mongo=Mongo()
		self.__db_msg=self.__config.getValue('Config','DB_MSG')
		self.__db_user=self.__config.getValue('Config','DB_USER')
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
			self.__mongo.saveUpdateOne({'chat_user':msg_username},{'$set':{'chat_id':msg_chat_id,'chat_type':msg_type,'chat_date':msg_date}},self.__db_user)
			self.__bot.sendMessage(msg_chat_id,"I have receieved your message!")
		MessageLoop(self.__bot,handle).run_as_thread()

	def start(self):
		try:
			print('server started...')
			while True:
				time.sleep(int(self.__config.getValue('Config','SLEEP_TIME')))
				print('process msgs')
				unsent_msgs=self.__mongo.find(self.__db_msg)
				idList=[]
				for msg in unsent_msgs:
					user_list=self.__mongo.find(self.__db_user,{'chat_user':msg['chat_user']})
					if len(user_list) == 0:
						raise TeleException(Type.NoneException,'No such user!'+username)
					else:
						self.__bot.sendMessage(user_list[0]['chat_id'],msg['chat_body'])
						idList.append(msg['_id'])
				self.__mongo.deleteMany(idList,self.__db_msg)
		except TeleException as te:
			LOGGER.error(str(te))


'''
main function
'''
if __name__=="__main__":
	server=Server()
	server.start()