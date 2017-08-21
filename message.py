#!/usr/bin/python

class Message:
	def __init__(self,type,title,body):
		self.__type=type
		self.__title=title
		self.__body=body

	def __str__(self):
		return print("**"+type+"**", ">**"+title+"**",body,sep="\n")