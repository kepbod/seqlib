import unittest
from interval import Interval


class TestInterval(unittest.TestCase):

    def setUp(self):
        self.a = [[1, 10, 'a'], [17, 22, 'b'], [7, 12, 'c'], [20, 25, 'd'],
                  [30, 35, 'e']]
        self.b = [[5, 12, 'I'], [20, 22, 'II'], [23, 28, 'III']]
        self.c = [[3, 7, 'I'], [10, 12, 'II'], [16, 20, 'III'], [23, 25, 'IV']]
        self.d = [[2, 4, 'a'], [2, 7, 'b'], [2, 3, 'c'], [4, 11, 'd'],
                  [4, 6, 'e'], [5, 9, 'f'], [7, 10, 'g'], [15, 17, 'h'],
                  [18, 21, 'i'], [9, 24, 'x'], [13, 14, 'y']]
        self.e = ['10', '15', 't']

    def testConvert(self):
        e = Interval(self.e)  # convert list to nested list
        self.assertListEqual(e.interval, [[10, 15, 't']], 'Failed in convert')

    def testInit(self):
        a = Interval(self.a)  # merge intervals
        self.assertListEqual(a.interval, [[1, 12, 'a', 'c'],
                                          [17, 25, 'b', 'd'], [30, 35, 'e']],
                             'Failed in initiation')

    def testAdd(self):
        self.a = Interval(self.a)  # self.a is an instance
        c = self.a + self.b
        self.assertListEqual(c.interval, [[1, 12, 'a', 'c', 'I'],
                                          [17, 28, 'b', 'd', 'II', 'III'],
                                          [30, 35, 'e']],
                             'Failed in c = a + b')
        c = self.b + self.a
        self.assertListEqual(c.interval, [[1, 12, 'a', 'c', 'I'],
                                          [17, 28, 'b', 'd', 'II', 'III'],
                                          [30, 35, 'e']],
                             'Failed in c = b + a')
        self.a += self.b
        self.assertListEqual(self.a.interval, [[1, 12, 'a', 'c', 'I'],
                                               [17, 28, 'b', 'd', 'II', 'III'],
                                               [30, 35, 'e']],
                             'Failed in a += b')

    def testMultiple(self):
        self.a = Interval(self.a)  # self.a is an instance
        c = self.a * self.b
        self.assertListEqual(c.interval, [[5, 12, 'a', 'c', 'I'],
                                          [20, 22, 'b', 'd', 'II'],
                                          [23, 25, 'b', 'd', 'III']],
                             'Failed in c = a * b')
        c = self.b * self.a
        self.assertListEqual(c.interval, [[5, 12, 'a', 'c', 'I'],
                                          [20, 22, 'b', 'd', 'II'],
                                          [23, 25, 'b', 'd', 'III']],
                             'Failed in c = b * a')
        self.a *= self.b
        self.assertListEqual(self.a.interval, [[5, 12, 'a', 'c', 'I'],
                                               [20, 22, 'b', 'd', 'II'],
                                               [23, 25, 'b', 'd', 'III']],
                             'Failed in a *= b')

    def testSubstract(self):
        self.a = Interval(self.a)  # self.a is an instance
        c = self.a - self.b
        self.assertListEqual(c.interval, [[1, 5, 'a', 'c'], [17, 20, 'b', 'd'],
                                          [22, 23, 'b', 'd'], [30, 35, 'e']],
                             'Failed in c = a - b')
        c = self.b - self.a
        self.assertListEqual(c.interval, [[25, 28, 'III']],
                             'Failed in c = b - a')
        self.a -= self.b
        self.assertListEqual(self.a.interval, [[1, 5, 'a', 'c'],
                                               [17, 20, 'b', 'd'],
                                               [22, 23, 'b', 'd'],
                                               [30, 35, 'e']],
                             'Failed in a -= b')

    def testInstanceAdd(self):
        self.a = Interval(self.a)  # self.a is an instance
        self.b = Interval(self.b)  # self.a is an instance
        c = self.a + self.b
        self.assertListEqual(c.interval, [[1, 12, 'a', 'c', 'I'],
                                          [17, 28, 'b', 'd', 'II', 'III'],
                                          [30, 35, 'e']],
                             'Failed in instance c = a + b')
        c = self.b + self.a  # TODO: why this addition did not change the order
        self.assertListEqual(c.interval, [[1, 12, 'a', 'c', 'I'],
                                          [17, 28, 'b', 'd', 'II', 'III'],
                                          [30, 35, 'e']],
                             'Failed in instance c = b + a')
        self.a += self.b
        self.assertListEqual(self.a.interval, [[1, 12, 'a', 'c', 'I'],
                                               [17, 28, 'b', 'd', 'II', 'III'],
                                               [30, 35, 'e']],
                             'Failed in instance a += b')

    def testInstanceMultiple(self):
        self.a = Interval(self.a)  # self.a is an instance
        self.b = Interval(self.b)  # self.b is an instance
        c = self.a * self.b
        self.assertListEqual(c.interval, [[5, 12, 'a', 'c', 'I'],
                                          [20, 22, 'b', 'd', 'II'],
                                          [23, 25, 'b', 'd', 'III']],
                             'Failed in instance c = a * b')
        c = self.b * self.a
        self.assertListEqual(c.interval, [[5, 12, 'I', 'a', 'c'],
                                          [20, 22, 'II', 'b', 'd'],
                                          [23, 25, 'III', 'b', 'd']],
                             'Failed in instance c = b * a')
        self.a *= self.b
        self.assertListEqual(self.a.interval, [[5, 12, 'a', 'c', 'I'],
                                               [20, 22, 'b', 'd', 'II'],
                                               [23, 25, 'b', 'd', 'III']],
                             'Failed in instance a *= b')

    def testInstanceSubstract(self):
        self.a = Interval(self.a)  # self.a is an instance
        self.b = Interval(self.b)  # self.b is an instance
        c = self.a - self.b
        self.assertListEqual(c.interval, [[1, 5, 'a', 'c'], [17, 20, 'b', 'd'],
                                          [22, 23, 'b', 'd'], [30, 35, 'e']],
                             'Failed in instance c = a - b')
        c = self.b - self.a
        self.assertListEqual(c.interval, [[25, 28, 'III']],
                             'Failed in instance c = b - a')
        self.a -= self.b
        self.assertListEqual(self.a.interval, [[1, 5, 'a', 'c'],
                                               [17, 20, 'b', 'd'],
                                               [22, 23, 'b', 'd'],
                                               [30, 35, 'e']],
                             'Failed in instance a -= b')

    def testSlice(self):
        self.a = Interval(self.a)
        self.assertEqual(self.a[1], [17, 25, 'b', 'd'], 'Failed in a[1]')
        self.assertListEqual(self.a[:2], [[1, 12, 'a', 'c'],
                                          [17, 25, 'b', 'd']],
                             'Failed in a[:2]')
        self.assertTrue([27, 34] in self.a, 'Failed in [27, 34] in a')
        self.assertTrue([31, 34] in self.a, 'Failed in [31, 34] in a')
        self.assertTrue([31, 37] in self.a, 'Failed in [31, 37] in a')
        self.assertTrue([27, 37] in self.a, 'Failed in [27, 37] in a')
        self.assertTrue([[27, 32], [33, 34]] in self.a,
                        'Failed in [[27, 32], [33, 34]] in a')
        self.assertTrue([[31, 32], [33, 34]] in self.a,
                        'Failed in [[31, 32], [33, 34]] in a')
        self.assertTrue([[31, 32], [33, 37]] in self.a,
                        'Failed in [[31, 32], [33, 37]] in a')
        self.assertTrue([[27, 32], [33, 37]] in self.a,
                        'Failed in [[27, 32], [33, 37]] in a')

    def testMapto(self):
        r = Interval.mapto(self.d, self.c)
        self.assertListEqual(r, [[3, 4, 'a', 'I'], [3, 7, 'b', 'I'],
                                 [4, 6, 'e', 'I'], [4, 7, 'd', 'I'],
                                 [5, 7, 'f', 'I'],
                                 [10, 11, 'd', 'II'], [10, 12, 'x', 'II'],
                                 [16, 20, 'x', 'III'], [16, 17, 'h', 'III'],
                                 [18, 20, 'i', 'III'], [23, 24, 'x', 'IV']],
                             'Failed in Mapto')

    def testOverlapwith(self):
        r = Interval.overlapwith(self.c, self.d)
        self.assertListEqual(r, [[3, 7, 'I', 'a', 'b', 'e', 'd', 'f'],
                                 [10, 12, 'II', 'd', 'x'],
                                 [16, 20, 'III', 'x', 'h', 'i'],
                                 [23, 25, 'IV', 'x']], 'Failed in Overlapwith')


if __name__ == '__main__':
    unittest.main()
