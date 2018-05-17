#!python
# -*- coding: utf-8 -*-#
#
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : Jan 4, 2017
# Update      : Aug 7, 2017 Mon
# 
# Imports
import os
from astropy.io import fits


def add_dev_exp_res():
    missing_bad =  [37, 38, 40, 65, 79, 80, 99, 102, 117, 129, 142, 
    164, 165, 177, 192, 11, 12, 18, 25, 27, 43, 48, 54, 61, 66, 88, 
    93, 94, 107, 110, 120, 126, 137, 145, 146, 149, 152, 161, 163, 
    167, 168, 175, 183, 195, 196]

    total = list(range(201))
    good = [t for t in total if (t not in missing_bad)]
    
    for i in good:
        d = getdata('galfit_outputs_f8/devauc/f814w_devauc{}.fits'.format(i))
        er = getdata('galfit_outputs_f8/expdisk_res/f814w_expdisk_res{}.fits'.format(i))
        data = d + er
        print(i)
        fits.writeto('bulge_disk_data/dev_exp_res/dev_exp_res{}.fits'.format(i),data,clobber=True)

        

if __name__ == "__main__":
    add_dev_exp_res()
