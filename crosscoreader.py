#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 10:13:38 2019

@author: singhsatyampratap
"""


from pysismo import pscrosscorr
import glob
import os
import warnings
# parsing configuration file to import dir of cross-corr results
from pysismo.psconfig import CROSSCORR_DIR



responsefrom = []
if USE_DATALESSPAZ:
    responsefrom.append('datalesspaz')
if USE_STATIONXML:
    responsefrom.append('xmlresponse')
OUTBASENAME_PARTS = [
    'xcorr',
    '-'.join(s for s in CROSSCORR_STATIONS_SUBSET) if CROSSCORR_STATIONS_SUBSET else None,
    '{}-{}'.format(FIRSTDAY.year, LASTDAY.year),
    '1bitnorm' if ONEBIT_NORM else None,
    '+'.join(responsefrom)
]
OUTFILESPATH = os.path.join(CROSSCORR_DIR, '_'.join(p for p in OUTBASENAME_PARTS if p))

print 'Default name of output files (without extension):\n"{}"\n'.format(OUTFILESPATH)
suffix = raw_input("Enter suffix to append: [none]\n")
if suffix:
    OUTFILESPATH = u'{}_{}'.format(OUTFILESPATH, suffix)
print 'Results will be exported to files:\n"{}" (+ extension)\n'.format(OUTFILESPATH)

# Reading inventories in dataless seed and/or StationXML files
dataless_inventories = []
if USE_DATALESSPAZ:
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        dataless_inventories = psstation.get_dataless_inventories(DATALESS_DIR,
                                                                  verbose=True)


xml_inventories = []
if USE_STATIONXML:
    xml_inventories = psstation.get_stationxml_inventories(STATIONXML_DIR,
                                                           verbose=True)
stations = psstation.get_stations(mseed_dir=MSEED_DIR,
                                  xml_inventories=xml_inventories,
                                  dataless_inventories=dataless_inventories,
                                  startday=FIRSTDAY,
                                  endday=LASTDAY,
                                  verbose=True)


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


# Plotting and exporting crashed data.
for pickle_file in pickle_files:
    print "\nProcessing cross-correlations of file: " + pickle_file
    xc = pscrosscorr.load_pickled_xcorr(pickle_file)
     # exporting to png file
    print "Exporting cross-correlations to file: {}.png".format(OUTFILESPATH)
    # optimizing time-scale: max time = max distance / vmin (vmin = 2.5 km/s)
    maxdist = max([xc[s1][s2].dist() for s1, s2 in xc.pairs()])
    maxt = min(CROSSCORR_TMAX, maxdist / 2.5)
    xc.plot(xlim=(-maxt, maxt), outfile=OUTFILESPATH + '.png', showplot=False)
    xc.export(outprefix=OUTFILESPATH, stations=stations, verbose=True)
