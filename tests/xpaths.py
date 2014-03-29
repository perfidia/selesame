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

	def testCorrectnesOfXPaths(self):
		d = selesame.analyze(url = "http://www.kinyen.pl/", driver = self.driver)

		for v in d.itervalues():
			for xpath in v:
				self.assertIsNotNone(self.driver.find_element_by_xpath(xpath))

	def testNumberOfLinksOnPage(self):
		d = selesame.analyze(url = self.getUrl("xpaths.html"), driver = self.driver)

		self.assertEqual(3, len(d['http://example.com/']))

	def testNumberOfLinksForId(self):
		d = selesame.get_same(url = self.getUrl("xpaths.html"), id = "a", driver = self.driver)

		self.assertEqual(3, len(d))

	def testNumberOfLinksForXPath(self):
		d = selesame.get_same(url = self.getUrl("xpaths.html"), xpath = '//*[@id="c"]', driver = self.driver)

		self.assertEqual(3, len(d))

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
