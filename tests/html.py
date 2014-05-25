import unittest
import os
import selesame
from selenium import webdriver

class Test(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

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

    def testNoHTMLTag(self):
        d = selesame.analyze(url = self.getUrl("nohtmltag.html"), driver = self.driver)

        for v in d.itervalues():
            for xpath in v:
                self.assertIsNotNone(self.driver.find_element_by_xpath(xpath))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
