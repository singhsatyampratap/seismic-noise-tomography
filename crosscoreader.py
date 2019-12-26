#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 10:13:38 2019

@author: singhsatyampratap
"""


from pysismo import pscrosscorr
import glob
import os

# parsing configuration file to import dir of cross-corr results
from pysismo.psconfig import CROSSCORR_DIR

# loading cross-correlations (looking for *.pickle files in dir *CROSSCORR_DIR*)
flist = sorted(glob.glob(os.path.join(CROSSCORR_DIR, 'xcorr*.pickle*')))
print 'Select file(s) containing cross-correlations to process: [All except backups]'
print '0 - All except backups (*~)'
print '\n'.join('{} - {}'.format(i + 1, os.path.basename(f))
                for i, f in enumerate(flist))

res = raw_input('\n')
if not res:
    pickle_files = [f for f in flist if f[-1] != '~']
else:
    pickle_files = [flist[int(i)-1] for i in res.split()]


# processing each set of cross-correlations
for pickle_file in pickle_files:
    print "\nProcessing cross-correlations of file: " + pickle_file
    xc = pscrosscorr.load_pickled_xcorr(pickle_file)
    maxt=1000
    xc.plot(xlim=(-maxt, maxt), outfile='SATYAM1' + '.png', showplot=False)
    