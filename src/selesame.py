#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from collections import deque
from collections import defaultdict
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver


def analyze(url=None, driver=None, mode="all"):
    """
    Analyze a given webpage and return list of elements with the same actions.

    Raise ValueError if url is None and condition equals True.

    :param url: text with url to analyze
    :type url: str
    :param driver: selenium driver with loaded page
    :type driver: WebDriver
    :param mode: defines way analyze function should work "all": Analize all, "href": analize only href, "onclick": analize only onclick
    :type mode: string
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
        target = node

        while (node.tag_name != "html"):
            node = node.find_element_by_xpath('..')
            xnodes.append(node.tag_name)

        xpath = ""

        n = 0
        for i in reversed(xnodes):
            if n < len(xnodes) - 1:
                xpath += "/%s" % i
            else:
                if i is not None:
                    xpath += "[contains(@href, %s)]" % i.replace(url, '')
            n += 1

        test = node.find_elements_by_xpath(xpath)

        if len(test):
            return xpath

        return get_exact_xpath(target)

    def get_exact_xpath(node):
        """
        :param node: WebElement took from selenium
        :type node: WebElement
        :return: xpath to a node
        :rtype: str
        """
        # extremely time consuming approach :(, not working in chrome

        debug = False

        if debug:
            print "ping",

        path = deque()

        while node.tag_name != 'html':
            p = node.find_element_by_xpath("..")
            d = defaultdict(int)
            elements = p.find_elements_by_xpath('*')
            for j in elements:
                d[j.tag_name] += 1
                if j.text == node.text:
                    path.appendleft(
                            "%s%s" % (j.tag_name, "[%s]" % d[j.tag_name] if d[j.tag_name] != 1 else "")
                    )
                    break
            node = p
            del d

        path.appendleft(node.tag_name)

        if debug:
            print "pong"

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

    condition = True
    if isinstance(driver, webdriver.Chrome):
        condition = driver.current_url == u'data:,'
    elif isinstance(driver, webdriver.Firefox):
        condition = driver.current_url == u'about:blank'

    if url is None and condition:
        raise ValueError("Provided URL is empty!")
    elif url:
        driver.get(url)

    # when server does a redirect the url is mismatched with actual site
    url = driver.current_url
    links = defaultdict(deque)
    if mode is "all" or mode is "href":
        nodes = driver.find_elements_by_tag_name('a')
        for node in nodes:
            links[node.get_attribute('href')].append(get_xpath(node, url))
    if mode is "all" or mode is "onclick":
        onclicks = driver.find_elements_by_xpath('//*[@onclick]')
        for script in onclicks:
            found = re.findall(r"location[ ]*=[ ]*'[^']+'", script.get_attribute('onclick'))
            for loc in found:
                href = loc.split("'")
                links[decorate_url(url, href[1])].append(get_xpath(script, url))

            found = re.findall(r'location[ ]*=[ ]*"[^"]+"', script.get_attribute('onclick'))
            for loc in found:
                href = loc.split('"')
                links[decorate_url(url, href[1])].append(get_xpath(script, url))

    if selfdriver:
        driver.quit()
    return links


def get_same(url=None, driver=None, id=None, xpath=None, mode="all"):
    """
    Analyze a given webpage and return a deque with elements that have the same action as the one in id/xpath.

    Raise ValueError if url is None and condition equals True.
    Raise ValueError if both id and xpath are None.
    Raise ValueError if href is None.

    :param url: text with url to analyze
    :type url: str
    :param driver: selenium driver with loaded page
    :type driver: WebDriver
    :param id: id of an element in a webpage
    :type id: str
    :param xpath: xpath to an element in a webpage (using selenium notation)
    :type xpath: str
    :param mode: defines way analyze function should work "all": Analize all, "href": analize only href, "onclick": analize only onclick
    :type mode: string
    :return: deque with elements with the same actions as the one in parameters
    :raises: ValueError
    """
    selfdriver = False
    if driver is None:
        # no parameter provided, create the default driver
        driver = webdriver.Chrome()
        selfdriver = True

    if url is None and driver.current_url == u'data:,':
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
    if href is None:
        found = re.findall(r"location[ ]*=[ ]*'[^']+'", element.get_attribute('onclick'))
        for loc in found:
            splited = loc.split("'")
            href = splited[1]

    if href is None:
        found = re.findall(r'location[ ]*=[ ]*"[^"]+"', element.get_attribute('onclick'))
        for loc in found:
            splited = loc.split('"')
            href = splited[1]

    if href is None:
        raise ValueError

    if not href.startswith("http://"):
        href = url + href

    links = analyze(url, driver, mode)

    same = links[href]

    if selfdriver:
        driver.quit()

    return same
