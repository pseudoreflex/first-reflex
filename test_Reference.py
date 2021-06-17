#!/usr/bin/env python3

import unittest
from Reference import (Reference)

class TestStringMethods(unittest.TestCase):

#        self.assertEqual('foo'.upper(), 'FOO')
#        self.assertTrue('FOO'.isupper())
#        self.assertFalse('Foo'.isupper())

#        s = 'hello world'
#        self.assertEqual(s.split(), ['hello', 'world'])
#        # check that s.split fails when the separator is not a string
#        with self.assertRaises(TypeError):
#            s.split(2)

    def test_ctor(self):
        context = Reference()
        self.assertFalse(None, context)

    def test_compile(self):
        context = Reference()
        context.compile("1/LDW + 1/P1 ~ 1/HDW + 1/H1")
        context.compile("1/HDW ~ 10/H1")
        # A lens is a pair for input projection
        # from and output collection to events
        context.compile("SquareSquare")
        context.compile("[(-1,0,0) (+1,0,0) (0,-1,0) (0,+1,0)]"+
                        "[(-1,0,0) (+1,0,0) (0,-1,0) (0,+1,0)]")
        self.assertFalse(None, context)

    def test_ftor(self):
        context = Reference()
        context.compile("1/LDW + 1/P1 ~ 1/HDW + 1/H1")
        context.compile("1/HDW ~ 10/H1")
        context.compile("SquareSquare")
        context.compile("[(-1,0,0) (+1,0,0) (0,-1,0) (0,+1,0)]"+
                        "[(-1,0,0) (+1,0,0) (0,-1,0) (0,+1,0)]")
        for i in range(10):
            context()
        self.assertFalse(None, context)

if __name__ == '__main__':
    unittest.main()
