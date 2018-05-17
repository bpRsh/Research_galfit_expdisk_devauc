#!python
# -*- coding: utf-8 -*-#
#
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : Jan 4, 2017
# Update      : Aug 7, 2017 Mon
# 
# Imports
import os
import subprocess
import glob
import re
import natsort
from astropy.io.fits import getdata
import numpy as np
import sys


def find_nan_in_fits(myfits):
    neg_idx = np.argwhere(dat.T < 0)
    print(neg_idx)
    
    if len(neg_idx) !=0:
        print('ERROR: Negative pixels found in: ', myfits)
        # sys.exit(1)
        negs.append(myfits)
               
    return negs
    

def check_path():
    bulge = 'bulge_disk_data/bulge_f8/f814w_bulge'
    disk = 'bulge_disk_data/disk_f8/f814w_disk'
    dev_exp_res = 'bulge_disk_data/dev_exp_res/dev_exp_res'
    
    # original galfit oututs
    devauc = 'galfit_outputs_f8/devauc/f814w_devauc'
    expdisk_res = 'galfit_outputs_f8/expdisk_res/f814w_expdisk_res'

    
    missing_bad =  [37, 38, 40, 65, 79, 80, 99, 102, 117, 129, 142, 
    164, 165, 177, 192, 11, 12, 18, 25, 27, 43, 48, 54, 61, 66, 88, 
    93, 94, 107, 110, 120, 126, 137, 145, 146, 149, 152, 161, 163, 
    167, 168, 175, 183, 195, 196]

    total = list(range(201))
    good = [t for t in total if (t not in missing_bad)]
    
    for g in good:
        myfits = dev_exp_res + str(g) + '.fits'
        print(g)
        find_nan_in_fits(myfits)
        


if __name__ == "__main__":
    check_path()
