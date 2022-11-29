import pypact as pp

SIMs = [
        ['/home/chen/Documents/research/WPSAE-DEMO/FISPACTII/data/EC/HCPB', 'inventory_1.out'],
       ]
PATH, NAME = SIMs[0]

with pp.Reader(f'{PATH}/{NAME}') as output:
  [print("Time {:.4E} (secs)".format(t.currenttime),
              "{:.4E} (days)".format(t.currenttime/3600/24),
              "{:.1E} (years)".format(t.currenttime/3600/24/365.25)) 
   for t in output.inventory_data]

timesteps = len(output.inventory_data)
print('timesteps', timesteps)

#times = []
for i, timestamp in enumerate(output):
   #times.append(timestamp.currenttime) #"Time {} (secs)".format(t.currenttime) 
   cool = timestamp.cooling_time
     
   print(f"{i+1}/{timesteps}:",
    "\n  t_cool {} (secs)".format(timestamp.cooling_time), 
         "{:.4E} (secs)".format(timestamp.cooling_time), 
         "{:.4E} (days)".format(timestamp.cooling_time/3600/24), 
         "{:.4E} (years)".format(timestamp.cooling_time/3600/24/365.25),
    "\n  t_dura {} (secs)".format(timestamp.duration), 
         "{:.4E} (secs)".format(timestamp.duration), 
         "{:.4E} (days)".format(timestamp.duration/3600/24), 
         "{:.4E} (years)".format(timestamp.duration/3600/24/365.25),
    "\n  t_irra {} (secs)".format(timestamp.irradiation_time),
         "{:.4E} (secs)".format(timestamp.irradiation_time), 
         "{:.4E} (days)".format(timestamp.irradiation_time/3600/24), 
         "{:.4E} (years)".format(timestamp.irradiation_time/3600/24/365.25),
    "\n  t_curr {} (secs)".format(timestamp.currenttime),
         "{:.4E} (secs)".format(timestamp.currenttime), 
         "{:.4E} (days)".format(timestamp.currenttime/3600/24), 
         "{:.4E} (years)".format(timestamp.currenttime/3600/24/365.25))
