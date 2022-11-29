# import the library
#import pypact as pp

# read the output file
#with pp.Reader('inventory.out') as output:
#  print(output.run_data.timestamp)
#  print(output.run_data.run_name)

import pypact as pp
import matplotlib.pyplot as plt
import numpy as np

import sys, os
filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '.', './data/EC/WCLL/inventory_10.out')
time = []
data = []

i = 0
with pp.Reader(filename) as output:
  for t in output.inventory_data:
    if not t.isirradiation:
      time.append(t.currenttime)
      data.append(t.gamma_heat)
      print(t.currenttime, t.gamma_heat)
    else:
      print(i,t.currenttime)
    i+=1

print(len(time))
year = 60*60*24*365.25
time = np.array(time)
time /= year
plt.plot(time, data)

plt.xscale('log')
plt.yscale('log')
plt.xlabel('time [year]')
plt.ylabel('heat')
plt.show()
