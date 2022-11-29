#!/usr/bin/env python3
# check pypact version: pip list
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
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import xlsxwriter
from matplotlib.ticker import FuncFormatter

DUMP = True
if (DUMP):
  import sys
  sys.path.append(os.path.abspath(r'/home/chen/Documents/numerical/python/packages'))
  import pypactQC as pp
else:
  import pypact as pp
#import pypact as pp
#help(pp)

PATH = f'/home/chen/Documents/research/WPSAE-DEMO/FISPACTII'
PATHo = PATH
PROPS = [('activity',r"Specific activity [Bq/cm$\mathbf{^3}$]"), ('heat',r"Decay heat [kW/cm$\mathbf{^3}$]"),('dose',r"Dose rate [Sv/h$\mathbf{\cdot}$cm$\mathbf{^3}$]")]

SIMs = [
[PATH, PATHo, 'EC', 'WCLL', PROPS,  [1,2,3,4,5,7,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]],
[PATH, PATHo, 'EC', 'HCPB', PROPS,  [1,2,3,4,7,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]],
[PATH, PATHo, 'Limiter', 'WCLL', PROPS, [1,2,3,4,5]],
[PATH, PATHo, 'Limiter', 'HCPB', PROPS, [1,2,3,4,5]],
]

MAX_TIMESTEPS = 200
TOP_NUCLIDES = 10
pulse = 48

yoff = 0
xoff = 0

LOG = True
CMAP = "gnuplot2_r"
SHOW_STABLE = False

SECS_IN_MIN = 60
SECS_IN_HOUR = 60 * 60
SECS_IN_DAY = 24 * SECS_IN_HOUR
SECS_IN_WEEK = 7 * SECS_IN_DAY
SECS_IN_MONTH = 30 * SECS_IN_DAY
SECS_IN_YEAR = 365.25 * SECS_IN_DAY
SECS_IN_DECADE = 10 * SECS_IN_YEAR
SECS_IN_CENTRY = 10 * SECS_IN_DECADE
SECS_IN_MILLENIUM = 10 * SECS_IN_CENTRY


def get_time_unit(time):
    if time < SECS_IN_MIN:
        return f"{time:.1f} s"
    if time < SECS_IN_HOUR:
        return f"{time/SECS_IN_MIN:.1f} mi"
    if time < SECS_IN_DAY:
        return f"{time/SECS_IN_HOUR:.1f} ho"
    if time < SECS_IN_WEEK:
        return f"{time/SECS_IN_DAY:.1f} da"
    if time < SECS_IN_MONTH:
        return f"{time/SECS_IN_WEEK:.1f} we"
    if time < SECS_IN_YEAR:
        return f"{time/SECS_IN_MONTH:.1f} mo"
    if time < SECS_IN_DECADE:
        return f"{time/SECS_IN_YEAR:.1f} ye"
    if time < SECS_IN_CENTRY:
        return f"{time/SECS_IN_DECADE:.1f} de"
    if time < SECS_IN_MILLENIUM:
        return f"{time/SECS_IN_CENTRY:.1f} c"
    return f"{time/SECS_IN_MILLENIUM:.1f} mi"


def add_margin(ymi, yma, margin):
  if (ymi <=0): ymi = 1e-12 
  dy = np.log10(yma)-np.log10(ymi)
  ymin = np.power(10, np.log10(ymi) - margin*dy -0.5*dy)
  ymax = np.power(10, np.log10(yma) + margin*dy)
  return ymin, ymax


def time_label(ymin, ymax):  
  #plt.annotate('1 day',rotation=90, ha='center',va='bottom', xy=(SECS_IN_DAY/SECS_IN_YEAR, ymin), xytext=(SECS_IN_DAY/SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.08)), 
  #        arrowprops=dict(alpha=0.5, fc='r', ec='r', headwidth=9, headlength=3))
  #plt.annotate('1 week',rotation=90, ha='center',va='bottom', xy=(SECS_IN_WEEK/SECS_IN_YEAR, ymin), xytext=(SECS_IN_WEEK/SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.08)), 
  #        arrowprops=dict(alpha=0.5, fc='r', ec='r', headwidth=9, headlength=3))
  #plt.annotate('1 month',rotation=90, ha='center',va='bottom', xy=(SECS_IN_MONTH/SECS_IN_YEAR, ymin), xytext=(SECS_IN_MONTH/SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.08)), 
  #        arrowprops=dict(alpha=0.5, fc='r', ec='r', headwidth=9, headlength=3))
  plt.text(1./SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.01), '1 second', fontweight='bold',rotation=90, ha='center',va='bottom')
  plt.text(5*60/SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.01), '5 minutes', fontweight='bold',rotation=90, ha='center',va='bottom')
  plt.text(30*60/SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.01), '30 minutes', fontweight='bold',rotation=90, ha='center',va='bottom')
  plt.text(SECS_IN_HOUR/SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.01), '1 hour', fontweight='bold',rotation=90, ha='center',va='bottom')
  plt.text(3*SECS_IN_HOUR/SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.01),'3 hours',fontweight='bold',rotation=90, ha='center',va='bottom')
  plt.text(5*SECS_IN_HOUR/SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.01),'5 hours',fontweight='bold',rotation=90, ha='center',va='bottom')
  plt.text(10*SECS_IN_HOUR/SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.01),'10 hours',fontweight='bold',rotation=90, ha='center',va='bottom')
  plt.text(SECS_IN_DAY/SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.01), '1 day', fontweight='bold',rotation=90, ha='center',va='bottom')
  plt.text(3*SECS_IN_DAY/SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.01), '3 days', fontweight='bold',rotation=90, ha='center',va='bottom')
  plt.text(SECS_IN_WEEK/SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.01), '1 week', fontweight='bold',rotation=90, ha='center',va='bottom')
  plt.text(2*SECS_IN_WEEK/SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.01), '2 weeks', fontweight='bold',rotation=90, ha='center',va='bottom')
  plt.text(4*SECS_IN_WEEK/SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.01), '4 weeks', fontweight='bold',rotation=90, ha='center',va='bottom')
  plt.text(8*SECS_IN_WEEK/SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.01), '8 weeks', fontweight='bold',rotation=90, ha='center',va='bottom')
  plt.text(6*SECS_IN_MONTH/SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.01), '6 months', fontweight='bold',rotation=90, ha='center',va='bottom')
  plt.text(SECS_IN_YEAR/SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.01), '1 year', fontweight='bold',rotation=90, ha='center',va='bottom')
  plt.text(10*SECS_IN_YEAR/SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.01), '10 years', fontweight='bold',rotation=90, ha='center',va='bottom')
  plt.text(50*SECS_IN_YEAR/SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.01), '50 years', fontweight='bold',rotation=90, ha='center',va='bottom')
  plt.text(100*SECS_IN_YEAR/SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.01), '100 years', fontweight='bold',rotation=90, ha='center',va='bottom')
  plt.text(1000*SECS_IN_YEAR/SECS_IN_YEAR, np.power(10,np.log10(ymin)+(np.log10(ymax)-np.log10(ymin))*0.01), '1000 years', fontweight='bold',rotation=90, ha='center',va='bottom')
  

def highlight_cell(x, y, ax=None, **kwargs):
    rect = plt.Rectangle((x - 0.5, y - 0.5), 1, 1, fill=False, **kwargs)
    ax = ax or plt.gca()
    ax.add_patch(rect)
    return rect


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


def dump(): 
      if (k==0):
        sheet1.write(k*4+0+yoff,0+1,'cooling time')
        sheet1.write(k*4+1+yoff,0+1,'cooling time')
  
        for i, data in enumerate(t_cool3):
          sheet1.write(k*4+0+yoff, i+2,'{:.2E}'.format(t_cool1[i]))
          sheet1.write(k*4+1+yoff, i+2, data)
      sheet1.write(k*1+2+yoff,0+1,f'{PROP}')
      sheet1.write(k*1+2+yoff,0+0,f'{NAME}')
  
      for i, data in enumerate(table):
        sheet1.write(k*1+2+yoff, i+2,'{:.2E}'.format(total[trunc:][data]))
      sheet2.write(k*3+0+yoff,0+0,f'{NAME}')
      sheet2.write(k*3+0+yoff,0+1,'cooling time')
      sheet2.write(k*3+1+yoff,0+1,'cooling time')
      sheet2.write(k*3+2+yoff,0+1,f'{PROP}')
  
      for i, data in enumerate(t_cool2):
        sheet2.write(k*3+0+yoff, i+2,'{:.2E}'.format(t_cool[i]))
        sheet2.write(k*3+1+yoff, i+2, data)
        sheet2.write(k*3+2+yoff, i+2,'{:.2E}'.format(total[trunc:][i]))

      if (DUMP) and (i_prop == len(PROPS)-1):
        tot_row = 0
        tot_row2 = 0
        sheet3.write(yoff,k*8+xoff,f'{NAME}')
        sheet4.write(yoff,k*8+xoff,f'{NAME}')
        for i, timestamp in enumerate(output):
          #print(f'  DUMP {i}')
          #dose = timestamp.dose_rate.dose
          #mass = timestamp.dose_rate.mass
          #print('==',timestamp.dose_rate.type, dose, mass, timestamp.dose_rate.distance)
          if (i < trunc -1):
            continue
          elif (i == trunc -1):
            time_base = timestamp.cooling_time
          else:
            time = timestamp.cooling_time - time_base
            sheet4.write(tot_row+1+yoff,k*8+xoff, get_time_unit(time))
            sheet4.write(tot_row+2+yoff,k*8+xoff,'Nuclide')
            sheet4.write(tot_row+2+yoff,k*8+1+xoff,'Activity')
            sheet4.write(tot_row+2+yoff,k*8+2+xoff,'% Error')
            sheet4.write(tot_row+2+yoff,k*8+3+xoff,'Heat')      
            sheet4.write(tot_row+2+yoff,k*8+4+xoff,'% Error')
            sheet4.write(tot_row+2+yoff,k*8+5+xoff,'Dose rate')      
            sheet4.write(tot_row+2+yoff,k*8+6+xoff,'% Error')

            for j, nuclide in enumerate(timestamp.nuclidesUE):
              name = nuclide.name
              heat = getattr(nuclide, 'heat')
              E_heat = getattr(nuclide, 'heat_Error')
              act   = getattr(nuclide, 'activity')
              E_act   = getattr(nuclide, 'activity_Error')
              dose   = getattr(nuclide, 'dose')
              E_dose   = getattr(nuclide, 'dose_Error')
              #print(f'  {i} {j} Nuclide: {name}', 'Activity: ','{:.3E}'.format(act), 'E(Activity)', '{:.2E}'.format(E_act), 'Heat: ', '{:.3E}'.format(heat),'E(heat):', '{:.2E}'.format(E_heat))
              #print(f'    Dose, {dose}, Dose_Error', '{:.2E}'.format(E_dose))

              sheet4.write(tot_row+j+3+yoff, k*8+xoff, name)
              sheet4.write(tot_row+j+3+yoff, k*8+1+xoff,'{:.3E}'.format(act))
              sheet4.write(tot_row+j+3+yoff, k*8+2+xoff,'{:.2E}'.format(E_act))
              sheet4.write(tot_row+j+3+yoff, k*8+3+xoff,'{:.3E}'.format(heat))
              sheet4.write(tot_row+j+3+yoff, k*8+4+xoff,'{:.2E}'.format(E_heat))
              sheet4.write(tot_row+j+3+yoff, k*8+5+xoff,'{:.3E}'.format(dose))
              sheet4.write(tot_row+j+3+yoff, k*8+6+xoff,'{:.2E}'.format(E_dose))
            sheet4.write(tot_row+j+4+yoff, k*8+0+xoff,'Total')
            sheet4.write(tot_row+j+4+yoff, k*8+1+xoff,'{:.3E}'.format(timestamp.total_activity))
            sheet4.write(tot_row+j+4+yoff, k*8+2+xoff,'{:.2E}'.format(timestamp.total_activity_error))
            sheet4.write(tot_row+j+4+yoff, k*8+3+xoff,'{:.3E}'.format(timestamp.total_heat))
            sheet4.write(tot_row+j+4+yoff, k*8+4+xoff,'{:.2E}'.format(timestamp.total_heat_error))
            sheet4.write(tot_row+j+4+yoff, k*8+5+xoff,'{:.3E}'.format(timestamp.total_gamma_dose_rate))
            sheet4.write(tot_row+j+4+yoff, k*8+6+xoff,'{:.2E}'.format(timestamp.total_gamma_dose_rate_error))
            tot_row+=j+4

            if (i in [trunc, trunc+13, trunc+17]):
              sheet3.write(tot_row2+1+yoff,k*8+xoff, get_time_unit(time))
              sheet3.write(tot_row2+2+yoff,k*8+0+xoff,'Nuclide')        	
              sheet3.write(tot_row2+2+yoff,k*8+1+xoff,'Activity')
              sheet3.write(tot_row2+2+yoff,k*8+2+xoff,'% Error')       
              sheet3.write(tot_row2+2+yoff,k*8+3+xoff,'Heat')      
              sheet3.write(tot_row2+2+yoff,k*8+4+xoff,'% Error')
              sheet3.write(tot_row2+2+yoff,k*8+5+xoff,'Dose rate')      
              sheet3.write(tot_row2+2+yoff,k*8+6+xoff,'% Error')

              for j, nuclide in enumerate(timestamp.nuclidesUE):
                name = nuclide.name
                heat = getattr(nuclide, 'heat')
                E_heat = getattr(nuclide, 'heat_Error')
                act   = getattr(nuclide, 'activity')
                E_act   = getattr(nuclide, 'activity_Error')
                dose   = getattr(nuclide, 'dose')
                E_dose   = getattr(nuclide, 'dose_Error')
                #print(f'  Nuclide: {name}', 'Activity: ','{:.3E}'.format(act), 'E(Activity)', '{:.2E}'.format(E_act), 'Heat: ', '{:.3E}'.format(heat),'E(heat):', '{:.2E}'.format(E_heat))
                sheet3.write(tot_row2+j+3+yoff, k*8+xoff, name)
                sheet3.write(tot_row2+j+3+yoff, k*8+1+xoff,'{:.3E}'.format(act))        	
                sheet3.write(tot_row2+j+3+yoff, k*8+2+xoff,'{:.2E}'.format(E_act))
                sheet3.write(tot_row2+j+3+yoff, k*8+3+xoff,'{:.3E}'.format(heat))
                sheet3.write(tot_row2+j+3+yoff, k*8+4+xoff,'{:.2E}'.format(E_heat))
                sheet3.write(tot_row2+j+3+yoff, k*8+5+xoff,'{:.3E}'.format(dose))
                sheet3.write(tot_row2+j+3+yoff, k*8+6+xoff,'{:.2E}'.format(E_dose))
              sheet3.write(tot_row2+j+4+yoff, k*8+xoff,'Total')
              sheet3.write(tot_row2+j+4+yoff, k*8+1+xoff,'{:.3E}'.format(timestamp.total_activity))
              sheet3.write(tot_row2+j+4+yoff, k*8+2+xoff,'{:.2E}'.format(timestamp.total_activity_error))
              sheet3.write(tot_row2+j+4+yoff, k*8+3+xoff,'{:.3E}'.format(timestamp.total_heat))
              sheet3.write(tot_row2+j+4+yoff, k*8+4+xoff,'{:.2E}'.format(timestamp.total_heat_error))
              sheet3.write(tot_row2+j+4+yoff, k*8+5+xoff,'{:.3E}'.format(timestamp.total_gamma_dose_rate))
              sheet3.write(tot_row2+j+4+yoff, k*8+6+xoff,'{:.2E}'.format(timestamp.total_gamma_dose_rate_error))
              tot_row2+=j+4


def plot():
      print(f'SIM {Dir}/{layer} {i_sim}/{len(SIMs)}; PROP {PROP} {i_prop}/{len(PROPS)}; ELEMENT num {k}/{len(Elements)}')
      filename = os.path.join(
      os.path.dirname(os.path.abspath(__file__)), f"{PATH}/data/{Dir}/{layer}", f"{infile}")
  
      fig, ax = plt.subplots(figsize=(8, 5))
      with pp.Reader(filename) as output:
        mat, nuclides, total, times, min_value, max_value = make_mat(output, prop=PROP, ax=ax)
        chosen = [ sum(x) for x in zip(*mat) ] # sum column
        other = np.array(total)-np.array(chosen)
  
        times = np.array(times)
        #print(f'  times {times[trunc-1]}')
        times -= times[trunc-1]
        t_cool = times[trunc:]
  
        #print(mat.shape)
        for i in range(len(nuclides)):
          #print(f'    nuclide  {i} / {len(range(TOP_NUCLIDES))}')
          #print(f'    {nuclides[i]}')
          plt.plot(times[trunc:]/SECS_IN_YEAR, mat[i,trunc:],'-o',label=f"{nuclides[i]}")

        plt.plot(times[trunc:]/SECS_IN_YEAR, total[trunc:],'k-o',lw=3, label='Total')
        plt.plot(times[trunc:]/SECS_IN_YEAR, other[trunc:],'k-o',label='Other')
  
        '''
        #verify total heat
        tot_heat = []
        data = output.inventory_data
        for d in data:
          tot_heat.append(d.total_heat)
          plt.plot(times[trunc:]/SECS_IN_YEAR, tot_heat[trunc:],'b--o',label='total')
        '''
  
      #titlestr = "log" if LOG else ""
      #plt.title(f"Top {TOP_NUCLIDES} ranked by {titlestr} {PROP}")
      plt.xlabel("Cooling time [years]", fontsize=14, fontweight='bold')
      plt.ylabel(f"{ylabel}", fontsize=14, fontweight='bold')
      plt.yscale('log')
      plt.xscale('log')
      #plt.axis([1e-3,5e2,1e-7,2e6])
 
      ymin, ymax = add_margin(min(total[trunc:]),max(total[trunc:]),0.05)
      plt.ylim(ymin,ymax) 
      plt.xlim(.05/SECS_IN_YEAR,)
      
      time_label(ymin, ymax)
      
      #ax = plt.gca()
      #ax.get_xaxis().set_major_formatter(plt.LogFormatter(10,  labelOnlyBase=False))
      #ax.get_yaxis().set_major_formatter(plt.LogFormatter(10,  labelOnlyBase=False))
      major_formatter = FuncFormatter(sci_format)
      ax.xaxis.set_major_formatter(major_formatter)
      ax.yaxis.set_major_formatter(major_formatter)
  
      plt.grid(alpha=0.3)
      plt.minorticks_on()
      plt.tick_params(which='both', direction='in', right=True, top = True, labelright=False)
      plt.legend()
  
      plt.tight_layout()
      plt.savefig(f'{PATHo}/figs/{Dir}/{layer}/{Dir}_{layer}_{PROP}_E{num}.png', format = 'png', dpi=300)
      #plt.show()
      plt.close()
      return t_cool, total, output
  

trunc = pulse*2+2
for i_sim, SIM in enumerate(SIMs):
  PATH, PATHo, Dir, layer, PROPS, Elements = SIM
  workbook = xlsxwriter.Workbook(f'{PATHo}/output/{Dir}_{layer}.xlsx')

  if (DUMP):
    sheet3 = workbook.add_worksheet(f'uncertainty')
    sheet4 = workbook.add_worksheet(f'uncertainty detail')

  for i_prop, (PROP,ylabel) in enumerate(PROPS):  
    sheet1 = workbook.add_worksheet(f'{PROP}')
    sheet2 = workbook.add_worksheet(f'{PROP} detail')
    for k, num in enumerate(Elements): 
      NAME = f'{layer}{num}'
      infile = f'inventory_{num}.out' 

      t_cool, total, output = plot()
      t_cool2 = [get_time_unit(i) for i in t_cool]
      #print('  times',t_cool)
      #print('  times', t_cool2)
      ## specify [0.1s, 1.0 day, 1. week, 12.2 mon, 10. year, 10 decade]
      table = [0,7,9,14,15,17]
      t_cool3 = [t_cool2[i] for i in table]
      t_cool1 = [t_cool[i] for i in table] 
      #dump(t_cool1, t_cool3)
      dump()

  workbook.close()
