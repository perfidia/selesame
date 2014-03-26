#!/usr/bin/env python
# -*- coding: utf-8 -*-

import selesame
from selenium import webdriver

if __name__ == '__main__':
    driver = webdriver.Firefox()
    r = selesame.analyze(url = "http://www.xitro.eu", driver = driver)
    print r
    driver.close()

    print selesame.get_same(url = "http://www.xitro.eu", xpath="/html/body/nav/ul/li/a[@href='http://xitro.eu/duplicated_script.html']")