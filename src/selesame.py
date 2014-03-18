#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from collections import defaultdict



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
    atags = driver.find_elements_by_tag_name('a')
    output = list()
    for a in atags:
        output.append({'href' : a.get_attribute('href'), 'webelement' : a})
    # you cannot extract xpath of already found element, so i've put object of WebElement inside dictionary (used
    # dictionaries it to better present result) maybe to get path to that WebElement object we should try to iterate
    # through parents until parent == html and then store concatenated path.
    #TODO: delete elements with href that don't exists > 1 time

    #code bellow shows dictionary of 'href' links and number of instances
    #DICTIONARY STRUCTURE { 'http://fc.put.poznan.pl/o-wydziale/dziekanat%2C45.html': 2 , ... }

    d = defaultdict(int)
    
    for links in output:
        d[links['href']] += 1
   
    #if you want to see the result, uncomment 2 lines bellow
    #for key in d:
    #    print key, " : ", d[key]
        
        

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
