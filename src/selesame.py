#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from collections import deque
from collections import defaultdict
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver

def analyze(url=None, driver=None):
    """
    Analyze a given webpage and return list of elements with the same actions.

    Raise ValueError if both url and driver are (not) None.
    ... description of other exceptions ...

    :param url: text with url to analyze
    :type url: str
    :param driver: selenium driver with loaded page
    :type driver: WebDriver
    :return: deque with elements with same actions (xpaths inside)
    :raises: ValueError
    """

    def get_xpath(node, url):
        """
        :param node: WebElement took from selenium
        :type node: WebElement
        :return: xpath to a node
        :rtype: str
        """

        id = node.get_attribute("id")

        if id:
            return '//*[@id="%s"]' % id

        xnodes = [node.get_attribute("href"), node.tag_name]

        while (node.tag_name != "html"):
            node = node.find_element_by_xpath('..')
            xnodes.append(node.tag_name)

        xpath = ""

        n = 0
        for i in reversed(xnodes):
            if n < len(xnodes) - 1:
                xpath += "/%s" % i
            else:
                if i != None:
                    xpath += "[contains(@href, %s)]" % i.replace(url, '')
            n+=1

        test = node.find_elements_by_xpath(xpath)

        if len(test) > 1 : return xpath
        else: return get_exact_xpath(node)


    def get_exact_xpath(node) :
        """
        :param node: WebElement took from selenium
        :type node: WebElement
        :return: xpath to a node
        :rtype: str
        """
        # extremely time consuming approach :(

        debug = False

        if debug: print "ping",

        path = deque()

        while node.tag_name != 'html':
            p = node.find_element_by_xpath("..")
            d = defaultdict(int)
            for j in p.find_elements_by_xpath('*'):
                d[j.tag_name] += 1
                if j.text == node.text:
                    path.appendleft(
                            "%s%s" % (j.tag_name, "[%s]" % d[j.tag_name] if d[j.tag_name] != 1 else "")
                    )
                    break
            node = p
            del d

        path.appendleft(node.tag_name)

        if debug: print "pong"

        return "/" + "/".join(path)

    #------------------------------------------------------

    def decorate_url(url, link):
        if not link.startswith("http://"):
            link = url + link
        return link

    #------------------------------------------------------

    selfdriver = False
    if driver is None:
        # no parameter provided, create the default driver
        driver = webdriver.Chrome()
        selfdriver = True
    # only checked in chrome
    if (url == None and driver.current_url == u'data:,'):
        raise ValueError("Provided URL is empty!")
    else:
        driver.get(url)
    # when server does a redirect the url is mismatched with actual site
    url = driver.current_url
    nodes = driver.find_elements_by_tag_name('a')
    onclicks = driver.find_elements_by_xpath('//*[@onclick]')
    links = defaultdict(deque)

    for node in nodes:
        links[node.get_attribute('href')].append(get_xpath(node, url))

    for script in onclicks:
        found = re.findall("location[ ]*=[ ]*'[^']+'", script.get_attribute('onclick'))
        for loc in found:
            href = loc.split("'")
            links[decorate_url(url, href[1])].append(get_xpath(script, url))

        found = re.findall('location[ ]*=[ ]*"[^"]+"', script.get_attribute('onclick'))
        for loc in found:
            href = loc.split('"')
            links[decorate_url(url, href[1])].append(get_xpath(script, url))

    if selfdriver:
        driver.quit()
    return links

def get_same(url=None, driver=None, id=None, xpath=None):
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
    :return: deque with elements with the same actions as the one in parameters
    :raises: ValueError
    """
    selfdriver = False
    if driver is None:
        # no parameter provided, create the default driver
        driver = webdriver.Chrome()
        selfdriver = True

    if (url == None and driver.current_url == u'data:,'):
        raise ValueError("Provided URL is empty!")
    else:
        driver.get(url)
    # when server does a redirect the url is mismatched with actual site
    url = driver.current_url

    if id is not None:
        element = driver.find_element_by_id(id)
    elif xpath is not None:
        try:
            element = driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            print "NoSuchElement"
    else:
        raise ValueError

    href = element.get_attribute('href')

    links = analyze(url, driver)

    same = links[href]

    if selfdriver:
        driver.quit()

    return same
