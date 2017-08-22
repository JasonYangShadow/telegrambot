#!/usr/bin/python

class Message:
	def __init__(self,type,title,body):
		self.__type=type
		self.__title=title
		self.__body=body

	def __str__(self):
		return '{0}\n,{1}\n,{2}\n'.format("<b>"+self.__type+"</b>","<i>"+self.__title+"</i>",self.__body)