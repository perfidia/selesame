#!/usr/bin/env python
# -*- coding: utf-8 -*-

import selesame
from selenium import webdriver

if __name__ == '__main__':
    driver = webdriver.Firefox()

    print "selesame.analyze()"
    print selesame.analyze(
            url = "http://www.xitro.eu",
            driver = driver
    )

    print

    print "selesame.get_same()"
    print selesame.get_same(
            url = "http://www.xitro.eu",
            driver = driver,
            xpath = "/html/body/footer/p"
    )

    driver.close()
