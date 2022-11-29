import os, sys
sys.path.append(os.path.abspath(r'/home/chen/Documents/numerical/python/packages'))
import pypactQC as pp

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '.', './data/EC/WCLL/inventory_10.out')

print('---------- pypactQC 1.3.5 ------------')

with pp.Reader(filename) as output:
  #for timestamp in output:
  for i, timestamp in enumerate(output[-1:]):
    attrs = vars(timestamp)
    print(',\n'.join("%s: %s" % item for item in attrs.items()))

    print(f'Time step: {i}')
    for nuclide in timestamp.nuclidesUE:
            name = nuclide.name
            heat = getattr(nuclide, 'heat')
            E_heat = getattr(nuclide, 'heat_Error')
            activity   = getattr(nuclide, 'activity')
            E_act   = getattr(nuclide, 'activity_Error')
           
            attrs = vars(nuclide)
            print(', '.join("%s: %s" % item for item in attrs.items()))
            print(f'Nuclide: {name}', 'Activity: ',f'{activity:.3E}', 'E(Activity)', '{:.2E}'.format(E_act), 'Heat: ', '{:.3E}'.format(heat),'E(heat):', '{:.2E}'.format(E_heat))
