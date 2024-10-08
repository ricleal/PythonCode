#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

Getting the child classes instantiating a the Base.
Every child must have a category name
A child class is instantiated from the Base with a category argument
'''

class Base(object):

	def __new__(cls, category, *arguments, **keywords):
		for subclass in Base.__subclasses__():
			if subclass.category == category:
				return super(cls, subclass).__new__(subclass, *arguments, **keywords)
		raise Exception, 'Category not supported!'


class ChildA(Base):
	category = 'A'

	def __init__(self, *arguments, **keywords):
		print 'Init for Category A', arguments, keywords

	def func(self):
		print 'func for Category A'


class ChildB(Base):
	category = 'B'

	def func(self):
		print 'func for Category B'

if __name__ == '__main__':
	"""
	Outputs:
	Init for Category A ('A',) {}
	func for Category A
	<class '__main__.ChildA'>
	func for Category B
	<class '__main__.ChildB'>
	"""
	a = Base('A')
	a.func()
	print type(a)
	b = Base('B')
	b.func()
	print type(b)
