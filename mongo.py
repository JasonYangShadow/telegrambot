#!/usr/bin/python
from pymongo import MongoClient
from pprint import pprint
from config import Config
from exception import Type,TeleException

class Mongo:
	def __init__(self,config_path=None):
		if config_path is None:
			self.__config=Config()
		else:
			self.__config=Config(config_path)
		self.__host=self.__config.getValue('Mongo','HOST')
		self.__port=self.__config.getValue('Mongo','PORT')
		self.__client=MongoClient(self.__host,int(self.__port))
		self.__db=self.__config.getValue('Mongo','DATABASE')
		self.__ct=self.__config.getValue('Mongo','COLLECTION')
		self.__database=None
		self.__collection=None

	def getDB(self,database=None):
		if database is None:
			self.__database=self.__client[self.__db]
			return self.__db
		else:
			self.__database=self.__client[database]
			return database

	def getCollection(self,collection=None):
		if self.__database is None:
			self.getDB()
		if collection is None:
			self.__collection=self.__database[self.__ct]
			return self.__ct
		else:
			self.__collection=self.__database[collection]
			return collection

	def insert(self,record,collection=None):
		if not isinstance(record, list):
			raise TeleException(Type.WrongTypeException,'record should be list') 
		self.getCollection(collection)
		return self.__collection.insert_many(record).inserted_ids

	def find(self,condition,collection=None):
		if not isinstance(condition,dict):
			raise TeleException(Type.WrongTypeException,'condition should be dict type')
		self.getCollection(collection)
		return list(self.__collection.find(condition))

	def exist(self,condition,collection=None):
		if not isinstance(condition,dict):
			raise TeleException(Type.WrongTypeException,'condition should be dict type')
		self.getCollection(collection)
		return True if self.__collection.count(condition)>0 else False 	

	def update(self,condition,update,collection=None):
		if not isinstance(condition,dict):
			raise TeleException(Type.WrongTypeException,'condition should be dict')
		if not isinstance(update,dict):
			raise TeleException(Type.WrongTypeException,'update should be dict')
		self.getCollection(collection)
		return self.__collection.update_many(condition,update)

	def saveUpdate(self,condition,update,collection=None):
		if not isinstance(condition,dict):
			raise TeleException(Type.WrongTypeException,'condition should be dict')
		if not isinstance(update,dict):
			raise TeleException(Type.WrongTypeException,'update should be dict')
		self.getCollection(collection)
		return self.__collection.update_many(condition,update,True)


	def saveUpdateOne(self,condition,update,collection=None):
		if not isinstance(condition,dict):
			raise TeleException(Type.WrongTypeException,'condition should be dict')
		if not isinstance(update,dict):
			raise TeleException(Type.WrongTypeException,'update should be dict')
		self.getCollection(collection)
		return self.__collection.update_one(condition,update,True)


