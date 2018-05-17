#!python
# -*- coding: utf-8 -*-#
#
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        :  Mar 21, 2018
# EstTime     : 10 secs

# Imports
from __future__ import division, unicode_literals, print_function
import numpy as np
from astropy.io import fits
import sys

# sys.stdout = open('file.txt', 'w')



b = np.array([-3,4])
d = np.array([1,-2])
db = d + b


# correct for bulge
bb = b.copy()
bbb = b.copy()
bb[bb<0] = 0
bbb[bbb>0] = 0
bulge = bb
disk = d + bbb

# correct for disk
dd = disk.copy()
ddd = disk.copy()
dd[dd<0] = 0
ddd[ddd>0] = 0
disk = dd
bulge = b + ddd


disk_bulge = disk + bulge



print("d = {}".format(d))
print("b = {}".format(b))
print("db = {}".format(db))
print("\n")
print("disk = {}".format(disk))
print("bulge = {}".format(bulge))
print("disk_bulge = {}".format(disk_bulge))
