# Galfit Basics:
# command: galfit INPUT_PARAMETER_FILE
# outputs: a) fit.log, galfit.01
#          b) imgblock.fits
#
# a) fit.log ==>  appended each time e.g. galfit.01, galfit.02
# b) imgblock.fits ==> it has 4 frames.
#                      0 is empty, 1 is input, 2 is model , 3 is residual.
#
#  command: ds9 -multiframe imgblock.fits
#  output : we can see 4 frames.
#
#
# command: galfit -o3 galfit.01 && rm -r galfit.01
# output : a) subcomps.fits
#
# a) subcomps.fits ==> it has two or more frames.
#                     0 is subcomps.fits, 1 is expdisk, 2 is devauc etc.
#
# INPUT_PARAMETER_FILE for galfit has two components:
#
# a) CONTROL PARAMETERS:  A-P     (these are compulsory)
# b) OBJECT PARAMETERS :  0-10 Z  (it should be at least one, e.g. devauc)
#
# a) CONTROL PARAMETERS
#        * These are fixed, not initial guesses.
#        * F: The row F is for masking
#            ic '1 0 %1 0 == ?'  INPUT_GALAXY  > mask.fits
#            If the bad pixel input file is a FITS image, all non-zero valued
#            pixels would be ignored during the fit. The pixel numbers where
#            value is 0 is only fitted.
#         * E: psf fine sampling factor is 2
#         * K: in my case plate scale is 0.06
#
# b) OBJECT PARAMETERS:
#         * These are initial guesses.
#         * Second column 1 means value not-fixed.
#         * Z: 0 fits the model, do not choose 1 while fitting.
#         * Better initial guess makes the simulation faster.
#           e.g. for f606w_gal0.fits  (from ds9 headers)
#           NAXIS1  =  601
#           NAXIS2  =  601
#
#           MAG     =  20.5874 # changes for galaxies
#           RADIUS  =  17.703  # changes for galaxies
#
#           PIXSCALE=  0.06 (for F814W galaxies)
#           MAG0    =  26.78212 (for f814)
#
#   Main commands : ic '1 0 %1 0 == ?'  INPUT_GALAXY  > mask.fits
#                 rm -r imgblock.fits subcomps.fits ; galfit three_comps.sh
#                 galfit -o3 galfit.01 && rm -r galfit.01
#                 ds9 -cmap a -scale log -multiframe imgblock.fits subcomps.fits &
#
# ic '1 0 %1 0 == ?'  /Users/poudel/jedisim/simdatabase/galaxies/f606w_gal107.fits  > mask.fits
# ds9 mask.fits /Users/poudel/jedisim/simdatabase/galaxies/f606w_gal107.fits &

# IMAGE and GALFIT CONTROL PARAMETERS
A) /Users/poudel/Research/a1_data/original_data/HST_ACS_WFC_f814w/sect23_f814w_gal2.fits 
B) imgblock.fits       # Output data image block
C) none                # Sigma image name (made from data if blank or "none")
D) f814w_psf.fits # Input PSF image and (optional) diffusion kernel
E) 2                   # PSF fine sampling factor relative to data
F) mask.fits           # Bad pixel mask (FITS image or ASCII coord list)
G) none                # File with parameter constraints (ASCII file)
H) 1 601 1 601         # Image region to fit (xmin xmax ymin ymax)
I) 200  200            # Size of the convolution box (x y)
J) 26.78212 # Magnitude photometric zeropoint
K) 0.06 0.06 # Plate scale (dx dy)    [arcsec per pixel]
O) regular             # Display type (regular, curses, both)
P) 0                   # Choose: 0=optimize, 1=model, 2=imgblock, 3=subcomps

# IMAGE and GALFIT OBJECT PARAMETERS
# Component number: 1
# Exponential function (concentration index n = 1)
# This gives disk profile.
0) expdisk            # Object type
1) 302.0 312.0 1 1         # position x, y        [pixel]
3) 21.1241 1         # total magnitude
4) 12.788 1         #     Rs               [Pixels]
9) 0.5        1       # axis ratio (b/a)
10) 100.0      1      # position angle (PA)  [Degrees: Up=0, Left=90]
Z) 0                  #  Skip this model in output image?  (yes=1, no=0)


# Component number: 2
# deVaucouleur function (concentration index n = 4)
# This gives the bulge profile.
0) devauc             # Object type
1) 302.0 312.0 1 1         # position x, y        [pixel]
3) 21.1241 1         # total magnitude
4) 12.788 1         #     R_e              [Pixels]
9) 0.5        1       # axis ratio (b/a)
10) 100.0       1     # position angle (PA)  [Degrees: Up=0, Left=90]
Z) 0                  #  Skip this model in output image?  (yes=1, no=0)
