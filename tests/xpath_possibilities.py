'''
Created on 29 Mar 2014

@author: perf
'''

import unittest
import os
import selesame
from selenium import webdriver

class Test(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.close()

    @classmethod
    def setUpClass(cls):
        path = os.getcwd().split(os.sep)

        for d in reversed(path[:]):
            if d != 'selesame':
                path.pop()
                continue

            break

        path.append("tests")
        path.append("www")

        cls.path = "file://" + os.sep.join(path)

    def getUrl(self, filename):
        return self.path + os.sep + filename

    def testHrefLinks(self):
        d = selesame.analyze(url = self.getUrl("index.html"), driver = self.driver, mode="href")
        prefix = self.driver.current_url.replace("index.html", "")
        self.assertEqual(1, len(d[prefix + 'test.html']))
        self.assertEqual(2, len(d[prefix + 'duplicated.html']))
        self.assertEqual(1, len(d[prefix + 'duplicated_script.html']))

    def testOnclickLinks(self):
        d = selesame.analyze(url = self.getUrl("index.html"), driver = self.driver, mode="onclick")
        prefix = self.driver.current_url.replace("index.html", "")
        self.assertEqual(0, len(d[prefix + 'test.html']))
        self.assertEqual(0, len(d[prefix + 'duplicated.html']))
        self.assertEqual(1, len(d[prefix + 'duplicated_script.html']))

    def testCombinedLinks(self):
        d = selesame.analyze(url = self.getUrl("index.html"), driver = self.driver, mode="all")
        prefix = self.driver.current_url.replace("index.html", "")
        self.assertEqual(1, len(d[prefix + 'test.html']))
        self.assertEqual(2, len(d[prefix + 'duplicated.html']))
        self.assertEqual(2, len(d[prefix + 'duplicated_script.html']))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
