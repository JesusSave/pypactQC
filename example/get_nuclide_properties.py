import os
#import pypact as pp

import sys
sys.path.append(os.path.abspath(r'/home/chen/Documents/numerical/python/packages'))
import pypactQC as pp

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '.', './data/EC/WCLL/inventory_10.out')

#from collections import defaultdict
#allnuclides = defaultdict()

with pp.Reader(filename) as output:
  #for timestamp in output:
  for i, timestamp in enumerate(output[-1:]):
    #attrs = vars(timestamp)
    #print(', '.join("%s: %s" % item for item in attrs.items()))

    print(f'{i}')
    for nuclide in timestamp.nuclidesUE:
            name = nuclide.name
            heat = getattr(nuclide, 'heat')
            E_heat = getattr(nuclide, 'heat_Error')
            activity   = getattr(nuclide, 'activity')
            E_act   = getattr(nuclide, 'activity_Error')
           
            attrs = vars(nuclide)
            print(', '.join("%s: %s" % item for item in attrs.items()))
            print(f'Nuclide: {name}')
            print('  Activity: ','{:.3E}'.format(activity))
            print('  E(Activity)', '{:.2E}'.format(E_act))
            print('  Heat: ', '{:.3E}'.format(heat))
            print('  E(heat):', '{:.2E}'.format(E_heat))
