#!python
# -*- coding: utf-8 -*-#
"""
Open files in ds9
    
@author: Bhishan Poudel
    
@date:  Mar 28, 2018
    
"""
# Imports
import os


def open_in_ds9():
    missing_bad =  [37, 38, 40, 65, 79, 80, 99, 102, 117, 129, 142, 
    164, 165, 177, 192, 11, 12, 18, 25, 27, 43, 48, 54, 61, 66, 88, 
    93, 94, 107, 110, 120, 126, 137, 145, 146, 149, 152, 161, 163, 
    167, 168, 175, 183, 195, 196]

    total = list(range(201))
    good = [t for t in total if (t not in missing_bad)]

    # ds9 commands
    ds9 = '/Applications/ds9.app/Contents/MacOS/ds9' + ' '
    
    # run ds9
    for g in good:
        print(g)
        b = 'galfit_outputs_f8/devauc/f814w_devauc{}.fits'.format(g)
        d = 'galfit_outputs_f8/expdisk_res/f814w_expdisk_res{}.fits'.format(g)
        files = b + ' ' + d
        cmd = ds9 + ' -height 1200 ' + ' -width 2500 ' + '-scale log -cmap a ' + files
        os.system(cmd)


if __name__ == "__main__":
    open_in_ds9()
