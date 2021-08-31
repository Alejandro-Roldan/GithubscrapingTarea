#!/usr/bin/env python

import unittest
from githubscraping import scrapeMain as scraping


class TestApp(unittest.TestCase):
    def test_001_Repositories(self):
        '''
            Test 001: scandirRecursive Python * Proxies * Repositories (gets extra data)
        '''
        input_json = 'test_001.json'
        output_json = 'out_test_001.json'
        scraping(input_json, output_json)

    def test_002_Issues(self):
        '''
            Test 002: python django-rest-framework jwt * Proxies * Issues
        '''
        input_json = 'test_002.json'
        output_json = 'out_test_002.json'
        scraping(input_json, output_json)

    def test_003_Wikis(self):
        '''
            Test 003: spark docker SQL * No proxies * Wikis
        '''
        input_json = 'test_003.json'
        output_json = 'out_test_003.json'
        scraping(input_json, output_json)

    def test_004_Unicode(self):
        '''
            Test 004: C の (japanese hiragana character "no") C++ * Testing Unicode compatibility * No proxies * Repositories (gets extra data)
        '''
        input_json = 'test_004.json'
        output_json = 'out_test_004.json'
        scraping(input_json, output_json)

    def test_005_For_Good_Measure(self):
        '''
            Test 005: openstack nova css * No proxies * Repositories (gets extra data)
        '''
        input_json = 'test_005.json'
        output_json = 'out_test_005.json'
        scraping(input_json, output_json)

def suite():
    suite = unittest.TestSuite()

    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestApp))

    return suite

 
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
