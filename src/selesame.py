#!/usr/bin/env python
# -*- coding: utf-8 -*-

def analyze(url = None, driver = None):
	"""
	Analyze a given webpage and return list of elements with the same actions.

	Raise ValueError if both url and driver are (not) None.
	... description of other exceptions ...

	:param url: text with url to analyze
	:type url: str
	:param driver: selenium driver with loaded page
	:type driver: WebDriver
	:return: list of tuples with elements with same actions (xpaths inside)
	:raises: ValueError
	"""

	pass

def get_same(url = None, driver = None, id = None, xpath = None):
	"""
	Analyze a given webpage and return a tuples with elements that have the same action as the one in id/xpath.

	Raise ValueError if both url and driver are (not) None.
	Raise ValueError if both id and xpath are (not) None.
	Raise ValueError if id or xpath does not exist.
	... description of other exceptions ...

	:param url: text with url to analyze
	:type url: str
	:param driver: selenium driver with loaded page
	:type driver: WebDriver
	:param id: id of an element in a webpage
	:type id: str
	:param xpath: xpath to an element in a webpage (using selenium notation)
	:type xpath: str
	:return: tuples with elements with the same actions as the one in parameters (xpaths inside, last xpath is a parameter)
	:raises: ValueError
	"""

	pass
