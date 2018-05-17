#!python
# -*- coding: utf-8 -*-#
#
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : 26-Oct-2016 13:10
# Last update :  Mar 20, 2018
# Est time    : 3 min for one galaxy one filter.
#
# Main commands : rm -rf imgblock.fits subcomps.fits ; galfit expdisk_devauc.sh
#                 galfit -o3 galfit.01 && rm -rf galfit.01
#                 ds9 -multiframe imgblock.fits subcomps.fits &

# Imports
from __future__ import division, unicode_literals, print_function
import string
from astropy.io import fits
import numpy as np
import subprocess
import time
import os
import sys


paramfile = r'expdisk_devauc.sh'


def replace_galfit_param(name, value, object_num=1, fixed=True):
    """Replace input galfit parameter file with new configuration.

    Arguments:

    name : parameter name, e.g. A-P,  1-10, 'Z'
    value: new value for the parameter in string form. e.g. '20.0'
    object_num: For A-Z object_num is 1
                For objects, object_num starts from 1.
    fixed: True means parameter will be fixed (0) during fitting.

    NOTE: Keep fixed = False while using this function to vary the parameter.
    """
    name, value = str(name), str(value)
    with open(paramfile) as f:
        galfit_file = f.readlines() 

    # Location of param.
    # 3rd column is where one can hold the parameters fixed (0) or allow vary 1
    loc = [i for i in range(len(galfit_file)) if
           galfit_file[i].strip().startswith(name + ')')][object_num - 1]
    param_str = galfit_file[loc]
    comment = param_str.find('#')
    if name in string.ascii_uppercase:
        fmt = '{}) {} {}'
        param_str = fmt.format(name, value, param_str[comment:])
    else:
        fmt = '{}) {} {}         {}'
        param_str = fmt.format(name, value, '0' if fixed else '1',
                               param_str[comment:])
    galfit_file[loc] = param_str
    with open(paramfile, 'w') as f:
        f.writelines(galfit_file)


def run_galfit(galaxy, band, outdir, count, centroid_file):
    """Run galfit on the input galaxy and create model and residual images.

    Runs galfit on the given input galaxies and creates model
        and residue images in the output directory

        galaxy        : path of input galaxy, e.g '/Users/poudel/Research/a1_data/original_data/HST_ACS_WFC_f814w'
        band          : band name of input galaxy, e.g f606w or f814w
        outdir        : output directory, e.g. galfit_outputs
        count         : count number of galaxy, e.g. 0 for f606w_gal0.fits
        cetnroid_file : input file having centroids of galaxies for given
                        band, e.g.
                        centroids_f6.csv, centroids_f8.csv
                        created by: find_centroid.py

        Needs  :
        input galaxy  : /Users/poudel/Research/a1_data/original_data/HST_ACS_WFC_f606w/sect23_f606w_gal0.fits
                        /Users/poudel/Research/a1_data/original_data/HST_ACS_WFC_f814w/sect23_f814w_gal0.fits
        output dir    : galfit_outputs/devauc
                        galfit_outputs/devauc_res
                        galfit_outputs/expdisk
                        galfit_outputs/expdisk_res
                        galfit_outputs/residual
        psf            : f606w_psf.fits
                         f606w_psf.fits
                         psf are created using TinyTim website
        mask           : mask.fits
                         ic '1 0 %1 0 == ?'  INPUT_GALAXY  > mask.fits
        paramfile      : expdisk_devauc.sh
                         input parameter file for galfit
                         (example from tar file of GALFIT website)
        centroid file  : a data file containing x,y position of input galaxy
                         it is created by find_centroid.py
                         right now, I have chosen the brightest pixel co-ordinate
                         to be the centroid of the galaxy. 
        Features:
        1. Following parameters on input paramfile for galfit will be updated:
           a) input galaxy name
           b) psf for that galaxy
           c) mask is created using ic command
           d) mag0,pixscale,mag,radius using astropy.fits.getval
           e) position or centroid using input file created from centroid.py
        2. Temporary files created in each loop
           a) mask.fits using ic '1 0 %1 0 == ?'  INPUT_GALAXY  > mask.fits
           b) imgblock.fits (0 is empty, 1 is input, 2 is model, 3 is residual)
           c) subcomps.fits (0 is input, 1 is expdisk, 2 is devauc etc.)

    """
    # galaxy = '/Users/poudel/Research/a1_data/original_data/HST_ACS_WFC_f814w'
    # band = f606w or f814w
    # ingal = '/Users/poudel/Research/a1_data/original_data/HST_ACS_WFC_f814w/sect23_f814w_gal0.fits'
    ingal = galaxy + '/' + 'sect23_' + band + '_gal' + str(count) + '.fits'
    psf = band + '_psf.fits'  # psf in the script directory

    #  get the value of magnitude, radius and mag0 of input galaxy
    mag = fits.getval(ingal, 'MAG')
    rad = fits.getval(ingal, 'RADIUS')
    mag0 = fits.getval(ingal, 'MAG0')

    #  MAG0 = 26.6611  for f606w band 
    #  MAG0 = 26.78212 for f814w band
    # pixscale  0.06 for both f606w and f814w
    PIXSCALE = '0.06 0.06'

    # find centroid of the input galaxy
    infile = centroid_file
    _, x, y = np.loadtxt(infile, unpack=True)
    centroid = str(x[count]) + ' ' + str(y[count]) + ' 1'

    # create galfit paramfile according to the input galaxy
    # For A-Z object_num is 1
    # fixed=True means it is fixed and not changed
    print("\n\n\n")
    print('+' * 80)
    print('+' * 80)
    print('+' * 80)
    print('{} {} {}'.format('Current Galaxy :  ', ingal, ''))
    print('+' * 80)
    print('+' * 80)
    print('+' * 80)

    # update control paramters
    replace_galfit_param('A', ingal,    object_num=1, fixed=False)
    replace_galfit_param('D', psf,      object_num=1, fixed=False)
    replace_galfit_param('J', mag0,     object_num=1, fixed=False)
    replace_galfit_param('K', PIXSCALE, object_num=1, fixed=False)

    # object 1 is expdisk
    replace_galfit_param('1', centroid, object_num=1, fixed=False)
    replace_galfit_param('3', mag,      object_num=1, fixed=False)
    replace_galfit_param('4', rad,      object_num=1, fixed=False)

    # object 2 is devauc
    replace_galfit_param('1', centroid, object_num=2, fixed=False)
    replace_galfit_param('3', mag,      object_num=2, fixed=False)
    replace_galfit_param('4', rad,      object_num=2, fixed=False)

    # create mask file according to the input galaxy
    # NOTE: in Control paramter of input paramfile:
    # F) mask.fits           # Bad pixel mask (FITS image or ASCII coord list)
    #
    # cmd = ic '1 0 %1 0 == ?'  FILENAME  > mask.fits
    cmd0 = "ic '1 0 %1 0 == ?'  " + ingal + "  > mask.fits"
    os.system(cmd0)

    # For objects, object_num starts from 1
    # 1 = expdisk, 2 = devauc

    # run galfit
    # rm -rf imgblock.fits subcomps.fits galfit.01 # removes these files.
    # galfit expdisk_devauc.sh  # gives galfit.01, imgblock.fits,if succeed.
    # galfit -o3 galfit.01      # runs only when galfit.01 exists
    # we can delete galfit.01 immediately after it it used.
    cmd1 = 'rm -rf galfit.01 imgblock.fits; galfit ' + paramfile
    cmd2 = 'rm -rf subcomps.fits; galfit -o3 galfit.01; rm -rf galfit.01'
    
    
    # run the command    
    os.system(cmd1) # gives galfit.01 if succeed


    # Error check
    # Just check once, some galaxies fails eg. 37, but we need to loop all.
    # if not os.path.isfile('galfit.01'):
    #     print('ERROR: File galfit.01 is missing.')
    #     sys.exit(1)

    if os.path.exists('galfit.01'):
        os.system(cmd2)
        
    # if os.path.isfile('galfit.02'):
    #     print('ERROR: File galfit.02 should not be here.')
    #     sys.exit(1)

    # get residual map from imgblock.fits
    residual = outdir + '/residual/' + band + '_res' + str(count) + '.fits'

    # expdisk from subcomps.fits ext = 1
    expdisk = outdir + '/expdisk/' + band + '_expdisk' + str(count) + '.fits'
    expdisk_res = outdir + '/expdisk_res/' + band + '_expdisk_res' + str(count) + '.fits'

    # devauc from subcomps.fits ext = 2 (NOTE: ext = 1 FOR ONE COMPONET FITTING)
    devauc = outdir + '/devauc/' + band + '_devauc' + str(count) + '.fits'
    devauc_res = outdir + '/devauc_res/' + band + '_devauc_res' + str(count) + '.fits'
    
    # Errror check
    # if not os.path.isfile('subcomps.fits'):
    #     print('ERROR: File subcomps.fits is missing.')
    #     sys.exit(1)
    # 
    # if not os.path.isfile('imgblock.fits'):
    #     print('ERROR: File imgblock.fits is missing.')
    #     sys.exit(1)
    

    # extracting frames of imgblock.fits and subcomps.fits if they exists.
    if os.path.isfile('subcomps.fits') and os.path.isfile('imgblock.fits'):
        # for imgblock.fits : 0 is empty, 1 is input, 2 is model, 3 is residual
        # for subcomps.fits: 0 is input, 1 is expdisk, 2 is devauc etc.

        # residual
        dat_res, hdr_res = fits.getdata(r'imgblock.fits', ext=3, header=True)
        hdr_res['MAG'] = mag
        hdr_res['MAG0'] = mag0
        hdr_res['RADIUS'] = rad
        hdr_res['PIXSCALE'] = 0.06
        hdr_res['PSF_INFO'] = 'PSF was created using TinyTim website.'
        hdr_res['CREATED'] = time.strftime("%a, %d %b %Y %H:%M:%S EDT", time.localtime())
        hdr_res['HISTORY'] = 'Created by Bhishan Poudel'
        fits.writeto(residual, dat_res, hdr_res, clobber=True)

        # expdisk
        dat_exp, hdr_exp = fits.getdata(r'subcomps.fits', ext=1, header=True)
        hdr_exp['MAG'] = mag
        hdr_exp['MAG0'] = mag0
        hdr_exp['RADIUS'] = rad
        hdr_exp['PIXSCALE'] = 0.06
        hdr_exp['PSF_INFO'] = 'PSF was created using TinyTim website.'
        hdr_exp['CREATED'] = time.strftime("%a, %d %b %Y %H:%M:%S EDT", time.localtime())
        hdr_exp['HISTORY'] = 'Created by Bhishan Poudel'
        fits.writeto(expdisk, dat_exp, hdr_exp, clobber=True)
        fits.writeto(expdisk_res, dat_exp + dat_res, hdr_exp, clobber=True)

        # devauc
        dat_dev, hdr_dev = fits.getdata(r'subcomps.fits', ext=2, header=True)
        hdr_dev['MAG'] = mag
        hdr_dev['MAG0'] = mag0
        hdr_dev['RADIUS'] = rad
        hdr_dev['PIXSCALE'] = 0.06
        hdr_dev['PSF_INFO'] = 'PSF was created using TinyTim website.'
        hdr_dev['CREATED'] = time.strftime("%a, %d %b %Y %H:%M:%S EDT", time.localtime())
        hdr_dev['HISTORY'] = 'Created by Bhishan Poudel'
        fits.writeto(devauc, dat_dev, hdr_dev, clobber=True)
        fits.writeto(devauc_res, dat_dev + dat_res, hdr_dev, clobber=True)


def main():
    """Main program."""
    # output directory without '/' in the end
    # ingal = '/Users/poudel/Research/a1_data/original_data/HST_ACS_WFC_f814w/sect23_f814w_gal0.fits'
    # ingal = galaxy + '/' + 'sec23_' + band + '_gal' + str(count) + '.fits'
    galaxy = '/Users/poudel/Research/a1_data/original_data/HST_ACS_WFC_f814w'
    galfit_outdir_f8 = 'galfit_outputs_f8'
    centroid_f8 = 'centroids_f8.csv'


    # outfolder
    odirs = ['expdisk', 'expdisk_res', 'devauc', 'devauc_res','residual']
    odirs = [ galfit_outdir_f8 + '/' + f for f in odirs]
    for od in odirs:
        if not os.path.isdir(od):
            os.makedirs(od)

    # run galfit for f814w band
    # for count in range(0, 200+1):
    for count in range(2,3):
        run_galfit(galaxy, 'f814w', galfit_outdir_f8, count, centroid_f8)

if __name__ == '__main__':
    
    # command: python run_galfit.py > /dev/null 2>&1 &

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
