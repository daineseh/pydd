import unittest

from pydd import BS

class TEST_BS_FORMAT_CHECKER(unittest.TestCase):
    def setUp(self):
        self._bs = BS()

    def test_case_1(self):
        expect = False
        result = self._bs.set_data('ZZ')
        self.assertEqual(expect, result)

    def test_case_2(self):
        expect = False
        result = self._bs.set_data('0MB')
        self.assertEqual(expect, result)

    def test_case_3(self):
        expect = False
        result = self._bs.set_data('1xx')
        self.assertEqual(expect, result)

    def test_case_4(self):
        expect = False
        result = self._bs.set_data('1o')
        self.assertEqual(expect, result)

    def test_case_5(self):
        expect = False
        result = self._bs.set_data('0')
        self.assertEqual(expect, result)

    def test_case_6(self):
        expect = True
        result = self._bs.set_data('11')
        self.assertEqual(expect, result)
