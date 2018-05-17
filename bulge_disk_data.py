#!python
# -*- coding: utf-8 -*-#
#
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        :  Mar 21, 2018
# EstTime     : 10 secs

# Imports
from __future__ import division, unicode_literals, print_function
import string
from astropy.io import fits
import numpy as np
import subprocess
import time
import os
import sys
import shutil

def add_hdr_galfit(galaxy, idir,odir,count):    
    # galfit outputs
    band = 'f814w'
    devauc = idir + '/devauc/' + band + '_devauc' + str(count) + '.fits'
    expdisk_res = idir + '/expdisk_res/' + band + '_expdisk_res' + str(count) + '.fits'

    
    #  mag, mag0, rad, pix from original stamp
    ingal = galaxy + '/' + 'sect23_' + band + '_gal' + str(count) + '.fits'
    mag = fits.getval(ingal, 'MAG')
    rad = fits.getval(ingal, 'RADIUS')
    mag0 = 26.78212
    pix = 0.06
    

    #===========================================================
    ##### read disk
    d, hdr = fits.getdata(expdisk_res, header=True)
    b = fits.getdata(devauc, header=False)
    hdr['MAG'] = mag
    hdr['MAG0'] = mag0
    hdr['RADIUS'] = rad
    hdr['PIXSCALE'] = pix
    hdr['PSF_INFO'] = 'PSF was created using TinyTim website.'
    hdr['CREATED'] = time.strftime("%a, %d %b %Y %H:%M:%S EDT", time.localtime())
    hdr['HISTORY'] = 'Created by Bhishan Poudel'
    
    
    # Make disk_res negative pixels positive and fix that in bulge
    # NOTE: d+b = disk + bulge
    dd = d.copy()
    ddd = d.copy()
    dd[dd<0] = 0
    ddd[ddd>0] = 0

    disk = dd
    bulge = b + ddd
    
    
    # zero small bulge
    bulge[bulge<1e-14] = 0
    
    # Create path to write files
    ofile_d = '{}/disk_f8/f814w_disk{}.fits'.format(odir,count)
    path_head,path_base = os.path.split(ofile_d)
    if not os.path.isdir(path_head):
        os.makedirs(path_head)
        

    # file path for bulge
    ofile_b =  '{}/bulge_f8/f814w_bulge{}.fits'.format(odir,count)
    path_head,path_base = os.path.split(ofile_b)
    if not os.path.isdir(path_head):
        os.makedirs(path_head)
    
    
    # write files
    fits.writeto(ofile_d, disk, hdr, overwrite=True)    
    fits.writeto(ofile_b, bulge, hdr, overwrite=True)
    
    # free memory
    del disk; del bulge; del hdr; del d; del b; del dd; del ddd

def main():
    """Main program."""
    # output directory without '/' in the end
    galaxy = '/Users/poudel/Research/a1_data/original_data/HST_ACS_WFC_f814w'
    idir = 'galfit_outputs_f8'
    odir = 'bulge_disk_data'
    
    if not os.path.isdir(odir):
        os.makedirs(odir)
        
    missing_bad =  [37, 38, 40, 65, 79, 80, 99, 102, 117, 129, 142, 
    164, 165, 177, 192, 11, 12, 18, 25, 27, 43, 48, 54, 61, 66, 88, 
    93, 94, 107, 110, 120, 126, 137, 145, 146, 149, 152, 161, 163, 
    167, 168, 175, 183, 195, 196]

    total = list(range(201))
    good = [t for t in total if (t not in missing_bad)]

    # run galfit for f814w band
    for g in good:
        print(g)
        add_hdr_galfit(galaxy, idir,odir,g)
        
    # for the missing or badly fitted galaxies,
    # choose original galaxy as the disk and null.fits as the bulge.
    for m in missing_bad:
        print(m)
        igal = '{}/sect23_f814w_gal{}.fits'.format(galaxy,m)
        
        # disk is the original galaxy
        odisk = '{}/disk_f8/f814w_disk{}.fits'.format(odir,m)
        shutil.copyfile(igal,odisk) # it has mag,mag0,rad,pix
        
        # for bulge
        obulge = '{}/bulge_f8/f814w_bulge{}.fits'.format(odir,m)
        dat,hdr = fits.getdata(igal, header=True)
        dat = np.zeros(dat.shape, dtype=np.float)
        fits.writeto(obulge,dat,hdr,overwrite=True)
        
if __name__ == '__main__':
    
    # beginning time
    program_begin_time = time.time()
    begin_ctime = time.ctime()

    # run main program
    main()

    # print the time taken
    program_end_time = time.time()
    end_ctime = time.ctime()
    seconds = program_end_time - program_begin_time
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    print('\nBegin time: ', begin_ctime)
    print('End   time: ', end_ctime, '\n')
    print("Time taken: {0:.0f} days, {1:.0f} hours, \
          {2:.0f} minutes, {3:f} seconds.".format(d, h, m, s))
