#!python
# -*- coding: utf-8 -*-#
#
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : Jan 4, 2017
# Last update : Feb 12, 2017
# Est time    :

# Imports
import os
import subprocess
import glob
import re
import natsort


def missing_galaxies(pth, num_gals):
    """Missing galaxies."""
    nums = natsort.natsorted([int(re.search('(.+?)(\d+)(\.\w*)', f).group(2))
                              for f in glob.glob(pth)])
    missing = [i for i in list(range(0, num_gals)) if i not in nums]
    return missing, len(missing)


def parse_fitlog(fitlog):
    """Find bad parameters and write them into a file."""
    # imports
    import re
    import numpy as np
    from natsort import natsorted

    # initialize variables
    ingal = None
    expdisk = None
    nums = []

    # parse fit.log
    with open(fitlog, 'r') as f:
        # read all lines of fit.log
        for line in f:
            # get input galaxy name
            # # */galaxies/f606w_gal0.fits[1:601,1:601]
            if line.strip().startswith("Input"):
                ingal = line[61:][0:-15]

            if '*' in line:
                bad = line
                num = re.search('(.+?)(\d+)(\.\w*)', ingal).group(2)
                nums.append(num)
                write = ingal + bad

        # list of  bad fitted galaxies
        bad = list(map(int, set(nums)))
        bad = natsort.natsorted(bad)

    return bad


def main(pth, log):
    # missing
    total = 201
    missing, nmissing = missing_galaxies(pth, total)

    # bad parameters
    bad = parse_fitlog(log)
    nbad = len(bad)
    missing_bad = missing + bad
    nmissing_bad = len(missing_bad)

    # summary of missing galaxies
    print(('band        = f814w'))
    print('Total       =', total)
    print('nmissing    = ', nmissing)
    print('nbad        = ', nbad)
    print('nmiss_bad   = ', nmissing_bad)
    print('missing     = ', missing)
    print('bad         = ', bad)
    print('missing_bad = ', missing_bad)


if __name__ == "__main__":
    pth = 'galfit_outputs_f8/residual/f8*.fits'
    log = 'fit_expdisk_devauc_f8.log'
    main(pth, log)
    
"""
band        = f814w
Total       = 201
nmissing    =  15
nbad        =  30
nmiss_bad   =  45
missing     =  [37, 38, 40, 65, 79, 80, 99, 102, 117, 129, 142, 164, 165, 177, 192]
bad         =  [11, 12, 18, 25, 27, 43, 48, 54, 61, 66, 88, 93, 94, 107, 110, 120, 126, 137, 145, 146, 149, 152, 161, 163, 167, 168, 175, 183, 195, 196]
missing_bad =  [37, 38, 40, 65, 79, 80, 99, 102, 117, 129, 142, 164, 165, 177, 192, 11, 12, 18, 25, 27, 43, 48, 54, 61, 66, 88, 93, 94, 107, 110, 120, 126, 137, 145, 146, 149, 152, 161, 163, 167, 168, 175, 183, 195, 196]
"""
