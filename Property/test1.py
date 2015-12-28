#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

'''

import unittest

class C(object):
    _p = 1
    
    def __init__(self):
        self._p = None
    
    @property
    def p(self):
        print 'getter'
        return self._p
    
    @p.setter
    def p(self, val):
        print 'setter'
        self._p = val
    
    @p.deleter
    def p(self):
        print 'deleter'
        del self._p


class TestStringMethods(unittest.TestCase):

  def test_c(self):
      c = C()
      c.p = 1
      self.assertEqual(c.p, 1)
      c.p = 2
      self.assertEqual(c.p, 2)
      


if __name__ == '__main__':
    unittest.main()