#!/usr/bin/env python
# -*- coding: utf-8 -*-

import selesame
from selenium import webdriver

if __name__ == '__main__':
    driver = webdriver.Chrome()
    r = selesame.analyze(url = "http://www.fc.put.poznan.pl", driver = driver)
    print r
    driver.close()
