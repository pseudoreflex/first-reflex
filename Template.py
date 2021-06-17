#!/usr/bin/env python3

from re import (findall, UNICODE)
from sys import (stdin, stdout, argv)
from math import (sqrt)
from numpy import (array, arange, int16, uint16, zeros)

__version__ = '0.0.1'

class Template(object):
    "example code for other modules"

    def __str__(self):
        "Represent template in string form"
        return("Template")

    def __init__(self, **kw):
        ""
        self.kw = kw
        self.time = 0
        print(argv[0]+" version: "+__version__)

    def __call__(self):
        "__call__ is the functor which increments time and acts on state."
        return(self)
