'''
Created on 29 Mar 2014

@author: perf
'''

import unittest
import selesame
from selenium import webdriver

class Test(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Firefox()

	def tearDown(self):
		#self.driver.close()
		pass

	def testXPath(self):
		d = selesame.analyze(url = "http://www.kinyen.pl/", driver = self.driver)

		for v in d.itervalues():
			for xpath in v:
				self.assertIsNotNone(self.driver.find_element_by_xpath(xpath))

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
