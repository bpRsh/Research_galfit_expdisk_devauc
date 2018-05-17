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


def find_all_negs_gals(mypath):
    negs=[]
    for i in range(201):
        try:
            dat = getdata('{}{}.fits'.format(mypath, i))
            print(i)
        except:
            dat = np.array([])
            
        mysum = np.sum(dat)
        fname = '{}{}.fits'.format(mypath, i)
            
        # check for neg pixel            
        neg_idx = np.argwhere(dat < 0)
        
        if len(neg_idx) != 0:
            # print("neg_idx = {}".format(neg_idx))
            print('ERROR: Negative Pixels found in: ', fname)
            negs.append(i)
        
            
    return negs

def check_path():
    bulge = 'bulge_disk_data/bulge_f8/f814w_bulge'
    disk = 'bulge_disk_data/disk_f8/f814w_disk'

    devauc      = 'galfit_outputs_f8/devauc/f814w_devauc'
    expdisk_res = 'galfit_outputs_f8/expdisk_res/f814w_expdisk_res'
    
    mypath = devauc
    mypath = expdisk_res
    
    # mypath = bulge
    # mypath = disk
    
    negs = find_all_negs_gals(mypath)
    print(negs)
    print(len(negs))



if __name__ == "__main__":
    check_path()
