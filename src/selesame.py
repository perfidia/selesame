#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from collections import defaultdict
from collections import deque

def getXPathFromNode(node):
    """

    :param node: WebElement took from selenium
    :return: xpath of WebElement
    """
    #TODO: transform nodes into xpath (hint: reverse array and read http://www.w3schools.com/XPath/xpath_syntax.asp)
    xnodes = [node.get_attribute("href"), node.tag_name]
    while (node.tag_name != "html"):
        node = node.parent()
        xnodes.append(node.tag_name)
    return node

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
    if driver is None:
        # no parameter provided, create the default driver
        driver = webdriver.Chrome()
    driver.get(url)
    nodes = driver.find_elements_by_tag_name('a')
    links = defaultdict(deque)
    for node in nodes:
        links[node.get_attribute('href')].append(getXPathFromNode(node))

    return links

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
