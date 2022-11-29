import re
import os

import pypact as pp
import pypact.analysis as ppa

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '.', './data/EC/WCLL/inventory_10.out')
                             
tz = ppa.TimeZone.COOL
properties = ['heat', 'grams', 'ingestion']
properties = ['activity']
isotopes = [ ppa.NuclideDataEntry(i) for i in ppa.get_all_isotopes() if ppa.find_z(i[0]) <= 10]

plt = ppa.LinePlotAdapter()

with pp.Reader(filename) as output:
    for p in properties:
        ppa.plotproperty(output=output,
                         property=p,
                         isotopes=isotopes,
                         plotter=plt,
                         fractional=True,
                         timeperiod=tz)
                         
    print( ppa.TimeZone.COOL)

plt.show()
