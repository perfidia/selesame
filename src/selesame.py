#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from collections import deque
from collections import defaultdict
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver

def analyze(url=None, driver=None, mode="all", unique=False):
    """
    Analyze a given webpage and return list of elements with the same actions.

    Raise ValueError if url is None and condition equals True.

    :param url: url of website that should be analyzed for same action elements. If none provided, loaded page of driver is used instead.
    :type url: str
    :param driver: selenium driver with or without loaded page
    :type driver: WebDriver
    :param mode: parameter to define what elements of loaded page should be scanned "all": Analyze all, "href": analyze only href links, "onclick": analyze only onclick location change
    :type mode: string
    :param unique: If true, analyze would also return elements with actions which occurred only once on loaded page
    :type unique: bool
    :return: defaultdict with elements with same actions. Key is target href and values are deque of xpaths.
    :rtype: defaultdict(deque)
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

        for n, i in enumerate(reversed(xnodes)):
            if n < len(xnodes) - 1:
                xpath += "/%s" % i
            else:
                if i is not None:
                    xpath += "[contains(@href, \"%s\")]" % i.replace(url, '')

        test = node.find_elements_by_xpath(xpath)

        if len(test) == 1:
            return xpath

        return get_exact_xpath(target)

    def get_exact_xpath(node):
        """
        :param node: WebElement took from selenium
        :type node: WebElement
        :return: xpath to a unique node
        :rtype: str
        """
        path = deque()
        check_children = True
        last_tag = node.tag_name
        array_used = False

        while node.tag_name != 'html':
            p = node.find_element_by_xpath("..")
            if check_children:
                d = defaultdict(int)
                elements = p.find_elements_by_xpath(last_tag)
                if len(elements) > 1:
                    array_used = True
                    for j in elements:
                        d[j.tag_name] += 1
                        if j.text == node.text and j.location == node.location:
                            path.appendleft("%s%s" % (j.tag_name, "[%s]" % d[j.tag_name]))
                            break
                else:
                    path.appendleft(elements[0].tag_name)
                    if (p.tag_name != 'html' and array_used): check_children = False
                last_tag = p.tag_name
                del d
            else: path.appendleft(node.tag_name)
            node = p

        path.appendleft(node.tag_name)

        return "/" + "/".join(path)

    #------------------------------------------------------

    def decorate_url(url, link):
        if not link.startswith("http://"):
            if url.endswith("/"):
                link = url + link
            else:
                link = url.rsplit('/', 1)[0] + "/" + link
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

    if not unique:
        removable = []
        for key in links:
            if len(links[key]) < 2: removable.append(key)
        for key in removable:
            del links[key]
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
        try:
            element = driver.find_element_by_id(id)
        except NoSuchElementException:
            raise ValueError("There are no existing elements with such id.")
    elif xpath is not None:
        try:
            element = driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            raise ValueError("There are no existing elements with such xpath.")
    else:
        raise ValueError("No id or xpath were provided.")

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
        raise ValueError("Selected element is not a link.")

    if not href.startswith("http://"):
        href = url + href

    links = analyze(url, driver, mode, True)

    same = links[href]

    if selfdriver:
        driver.quit()

    return same
