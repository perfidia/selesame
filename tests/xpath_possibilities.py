'''
Created on 12 May 2014

@author: xitro
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
        d = selesame.analyze(url=self.getUrl("index.html"), driver=self.driver, mode="href", unique=True)
        prefix = self.driver.current_url.replace("index.html", "")
        self.assertEqual(1, len(d[prefix + 'test.html']))
        self.assertEqual(2, len(d[prefix + 'duplicated.html']))
        self.assertEqual(1, len(d[prefix + 'duplicated_script.html']))

    def testOnclickLinks(self):
        d = selesame.analyze(url=self.getUrl("index.html"), driver=self.driver, mode="onclick", unique=True)
        prefix = self.driver.current_url.replace("index.html", "")
        self.assertEqual(0, len(d[prefix + 'test.html']))
        self.assertEqual(0, len(d[prefix + 'duplicated.html']))
        self.assertEqual(1, len(d[prefix + 'duplicated_script.html']))

    def testCombinedLinks(self):
        d = selesame.analyze(url=self.getUrl("index.html"), driver=self.driver, mode="all", unique=True)
        prefix = self.driver.current_url.replace("index.html", "")
        self.assertEqual(1, len(d[prefix + 'test.html']))
        self.assertEqual(2, len(d[prefix + 'duplicated.html']))
        self.assertEqual(2, len(d[prefix + 'duplicated_script.html']))

    def testCombinedUniqueLinks(self):
        d = selesame.analyze(url=self.getUrl("index.html"), driver=self.driver, mode="all", unique=False)
        prefix = self.driver.current_url.replace("index.html", "")
        self.assertEqual(0, len(d[prefix + 'test.html']))
        self.assertEqual(2, len(d[prefix + 'duplicated.html']))
        self.assertEqual(2, len(d[prefix + 'duplicated_script.html']))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
