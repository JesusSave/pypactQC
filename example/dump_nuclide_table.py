#!/usr/bin/env python3
# pypact >= 1.3.5, install as:
'''
git clone https://github.com/fispact/pypact
cd pypact
pip3 install .
'''
"""
    times -= times[trunc-1]
    Make a heatmap like plot (imshow) with a sliding window over
    time series data
"""
import os
import math
from collections import defaultdict
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import xlsxwriter

DUMP = True
if (DUMP):
  import sys
  sys.path.append(os.path.abspath(r'/home/chen/Documents/numerical/python/packages'))
  import pypactQC as pp
else:
  import pypact as pp

PATH = f'/home/chen/Documents/research/WPSAE-DEMO/FISPACTII'
PATHo = PATH
########PROPS = [('activity',r"Specific activity [Bq/cm$^3$]"), ('heat',r"Decay heat [kW/cm$^3$]"),('dose',r"Dose rate [Sv/hr]")]
PROPS = [('activity',r"Specific activity [Bq/cm$^3$]"), ('heat',r"Decay heat [kW/cm$^3$]")]
PLANKETS = ['HCPB', 'WCLL']

SIMs = [
[PATH, PATHo, 'Limiter', PLANKETS, PROPS, [1,2,3,4,5]],
[PATH, PATHo, 'EC', PLANKETS, PROPS,  [1,2,3,4,5,7,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]],
#[PATH, PATHo, 'EC', PLANKETS, PROPS,  [1,2, 3]],
]

MAX_TIMESTEPS = 200
TOP_NUCLIDES = 10
pulse = 48

yoff = 0
xoff = 0

LOG = False
LOG = True
CMAP = "gnuplot2_r"
SHOW_STABLE = False

SECS_IN_MIN = 60
SECS_IN_HOUR = 60 * 60
SECS_IN_DAY = 24 * SECS_IN_HOUR
SECS_IN_WEEK = 7 * SECS_IN_DAY
SECS_IN_2WEEK = 2 * SECS_IN_WEEK
SECS_IN_MONTH = 30 * SECS_IN_DAY
SECS_IN_YEAR = 365.25 * SECS_IN_DAY
SECS_IN_DECADE = 10 * SECS_IN_YEAR
SECS_IN_CENTRY = 10 * SECS_IN_DECADE
SECS_IN_MILLENIUM = 10 * SECS_IN_CENTRY


def get_time_unit(time):
    if time < SECS_IN_MIN:
        return f"{time:g} s"
    if time < SECS_IN_HOUR:
        return f"{time/SECS_IN_MIN:g} min"
    if time < SECS_IN_DAY:
        return f"{time/SECS_IN_HOUR:g} h"
    if time < SECS_IN_WEEK:
        return f"{time/SECS_IN_DAY:g} d"
    if time < SECS_IN_2WEEK:
        return f"{time/SECS_IN_WEEK:g} week"
    if time < SECS_IN_MONTH:
        return f"{time/SECS_IN_WEEK:g} weeks"
    if time < SECS_IN_YEAR:
        return f"{time/SECS_IN_MONTH:.1f} months"
    else:
        return f"{time/SECS_IN_YEAR:.0f} years"


def make_mat(output, ax=None, prop="atoms"):
    min_value, max_value = 0.0, 0.0
    nuclides = sorted_top_nuclides(output, ntop=TOP_NUCLIDES, prop=prop)
    ntimesteps = min(MAX_TIMESTEPS, len(output))
    mat = np.zeros((ntimesteps, TOP_NUCLIDES + 1))
    times = []
    total = []
    for i, timestamp in enumerate(output[:ntimesteps]):
        #times.append(get_time_unit(timestamp.currenttime))
        #times.append(timestamp.duration)
        times.append(timestamp.cooling_time)
        tot = 0
        for j, nuclide in enumerate(timestamp.nuclides):
            tot+= getattr(nuclide, prop)
            # find index of nuclide in sorted nuclides
            index = next(
                (n for n, item in enumerate(nuclides) if item == nuclide.name),
                -1,
            )

            if index == -1:
                continue
            mat_value = getattr(nuclide, prop)

            min_value = min(min_value, mat_value)
            max_value = max(max_value, mat_value)
            mat[i, index] = mat_value
            #highlight_cell(i, index, ax=ax, color="k", linewidth=1)
            
        total.append(tot)
    return mat.T, nuclides, total, times, min_value, max_value


def sorted_top_nuclides(output, ntop=100, prop="atoms"):
    allnuclides = defaultdict()
    for timestamp in output:
        for nuclide in timestamp.nuclides:
            name = nuclide.name
            value = getattr(nuclide, prop)
            # ignore unstable nuclides which have short halflives
            # compared to the timestep - take 10% of timestep here as cutoff
            show_stable = SHOW_STABLE and nuclide.half_life == 0.0
            if value > 0 and (
                (nuclide.half_life > timestamp.duration * 0.1) or show_stable
            ):
                allnuclides[name] = max(allnuclides.get(name, 0), value)

    # sort nuclides based on the property
    sortednuclides = sorted(allnuclides, key=allnuclides.get, reverse=True)
    return sortednuclides[:ntop]


def sci_format(x,lim):
  return '{:.1E}'.format(x)

def rows(blanket, k):
  #print(f'SIM {Dir}/{blanket} {i_sim}/{len(SIMs)}; PROP {PROP} {i_prop}/{len(PROPS)}; ELEMENT num {k}/{len(Elements)}')
  filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{PATH}/data/{Dir}/{blanket}", f"{infile}")

  with pp.Reader(filename) as output:
    mat, nuclides, total, times, min_value, max_value = make_mat(output, prop=PROP, ax=None)
    chosen = [ sum(x) for x in zip(*mat) ] # sum column
    other = np.array(total)-np.array(chosen)
    times = np.array(times)
    times -= times[trunc-1]
    t_cool = times[trunc:]

  rows = []
  for i, timestamp in enumerate(output):
    if (i < trunc -1):
      continue
    elif (i == trunc -1):
      time_base = timestamp.cooling_time
    else:
      time = timestamp.cooling_time - time_base
      row = len(timestamp.nuclidesUE)
      rows.append(row)
  return rows

def table_dump(tot_row):
  print(f'SIM {Dir}/{blanket} {i_sim}/{len(SIMs)}; PROP {PROP} {i_prop}/{len(PROPS)}; ELEMENT num {k}/{len(Elements)}')
  filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{PATH}/data/{Dir}/{blanket}", f"{infile}")

  with pp.Reader(filename) as output:
    mat, nuclides, total, times, min_value, max_value = make_mat(output, prop=PROP, ax=None)
    chosen = [ sum(x) for x in zip(*mat) ] # sum column
    other = np.array(total)-np.array(chosen)
    times = np.array(times)
    times -= times[trunc-1]
    t_cool = times[trunc:]

    if (blanket=='HCPB'):
      b = 0
    elif (blanket=='WCLL'):
      b = 3
    else:
      print('Error: blanket confusion')
      exit()
    sheet1.write(tot_row+ yoff,b+xoff, f'{blanket}{k+1}')
    sheet1.write(tot_row+ yoff,6+b+xoff, f'{blanket}{k+1}')

    ii = 0
    for i, timestamp in enumerate(output):
      if (i < trunc -1):
        continue
      elif (i == trunc -1):
        time_base = timestamp.cooling_time
      else:
        time = timestamp.cooling_time - time_base
        if (rows_HCPB[ii]==0) and (rows_WCLL[ii]==0):
          continue
        if (ii==0):
          tot_row += 0
        else:
          tot_row += max(rows_HCPB[ii-1], rows_WCLL[ii-1]) + 3
        ii += 1

        sheet1.write(tot_row+1+yoff,xoff, get_time_unit(time))

        sheet1.write(tot_row+2+yoff,b+0+xoff,'Nuclide')                
        sheet1.write(tot_row+2+yoff,b+1+xoff,'Activity\n[Bq/cm^3]')
        sheet1.write(tot_row+2+yoff,b+2+xoff,'Error [%]')       

        sheet1.write(tot_row+2+yoff,b+0+6+xoff,'Nuclide')                
        sheet1.write(tot_row+2+yoff,b+1+6+xoff,'Decay Heat\n [Bq/cm^3]')      
        sheet1.write(tot_row+2+yoff,b+2+6+xoff,'Error [%]')

        for j, nuclide in enumerate(timestamp.nuclidesUE):
          name = nuclide.name
          heat = getattr(nuclide, 'heat')
          E_heat = getattr(nuclide, 'heat_Error')
          act   = getattr(nuclide, 'activity')
          E_act   = getattr(nuclide, 'activity_Error')
          dose   = getattr(nuclide, 'dose')
          E_dose   = getattr(nuclide, 'dose_Error')
          print(f'  {i} {j} Nuclide: {name}', 'Activity: ','{:.3E}'.format(act), 'E(Activity)', '{:.2E}'.format(E_act), 'Heat: ', '{:.3E}'.format(heat),'E(heat):', '{:.2E}'.format(E_heat))
          print(f'    Dose, {dose}, Dose_Error', '{:.2E}'.format(E_dose))

          sheet1.write(tot_row+j+3+yoff, b+0+xoff, name)
          sheet1.write(tot_row+j+3+yoff, b+1+xoff,'{:.3E}'.format(act))
          sheet1.write(tot_row+j+3+yoff, b+2+xoff,'{:.2E}'.format(E_act))
          sheet1.write(tot_row+j+3+yoff, b+0+6+xoff, name)
          sheet1.write(tot_row+j+3+yoff, b+1+6+xoff,'{:.3E}'.format(heat))
          sheet1.write(tot_row+j+3+yoff, b+2+6+xoff,'{:.2E}'.format(E_heat))

        if (nuclide.name == None):
          sheet1.write(tot_row+j+2+yoff, b+0+xoff,'Total')
          sheet1.write(tot_row+j+2+yoff, b+0+1+xoff,'{:.3E}'.format(timestamp.total_activity))
          sheet1.write(tot_row+j+2+yoff, b+0+2+xoff,'{:.2E}'.format(timestamp.total_activity_error))
          sheet1.write(tot_row+j+2+yoff, b+6+0+xoff,'Total')
          sheet1.write(tot_row+j+2+yoff, b+6+1+xoff,'{:.3E}'.format(timestamp.total_heat))
          sheet1.write(tot_row+j+2+yoff, b+6+2+xoff,'{:.2E}'.format(timestamp.total_heat_error))
        else:
          sheet1.write(tot_row+j+4+yoff, b+0+xoff,'Total')
          sheet1.write(tot_row+j+4+yoff, b+0+1+xoff,'{:.3E}'.format(timestamp.total_activity))
          sheet1.write(tot_row+j+4+yoff, b+0+2+xoff,'{:.2E}'.format(timestamp.total_activity_error))
          sheet1.write(tot_row+j+4+yoff, b+6+0+xoff,'Total')
          sheet1.write(tot_row+j+4+yoff, b+6+1+xoff,'{:.3E}'.format(timestamp.total_heat))
          sheet1.write(tot_row+j+4+yoff, b+6+2+xoff,'{:.2E}'.format(timestamp.total_heat_error))
    if (nuclide.name == None):
      last_row = tot_row+j+2
    else:
      last_row = tot_row+j+4
  return last_row

trunc = pulse*2+2
for i_sim, SIM in enumerate(SIMs):
  PATH, PATHo, Dir, BLANKETS, PROPS, Elements = SIM
  workbook = xlsxwriter.Workbook(f'{PATHo}/output/table_{Dir}.xlsx')

  if (DUMP):
    sheet1 = workbook.add_worksheet(f'Table')

  for i_blanket, blanket in enumerate(BLANKETS):
    TOT_row = 0
    for i_prop, (PROP,ylabel) in enumerate(PROPS):  
      if (i_prop>0):
          continue
      for k, num in enumerate(Elements): 
        NAME = f'{blanket}{num}'
        infile = f'inventory_{num}.out' 
        try:
          rows_HCPB = rows('HCPB',num)
        except:
          rows_HCPB = 0*np.ones(18)
        try:
          rows_WCLL = rows('WCLL',num)
        except:
          rows_WCLL = 0*np.ones(18)
        print(f'    HCPB ELEMENT num {k}/{len(Elements)}', rows_HCPB)
        print(f'    WCLL ELEMENT num {k}/{len(Elements)}', rows_WCLL)
        try:
          table_dump(TOT_row)
        except:
          pass

        t_row = 0
        for i_row, r_HCPB in enumerate(rows_HCPB):
          if (rows_HCPB[i_row]==0) and (rows_WCLL[i_row]==0):
            continue
          t_row += max(r_HCPB, rows_WCLL[i_row]) +3 
        TOT_row += t_row+1

        #t_cool2 = [get_time_unit(i) for i in t_cool]
        #print('  times', t_cool2)
        #table = [0,7,9,14,15,17]
        #t_cool3 = [t_cool2[i] for i in table]
        #t_cool1 = [t_cool[i] for i in table] 
  workbook.close()
