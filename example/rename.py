import os

NTMIN = 2000
NTMAX = 4000
DT = 20

#for i in range((NTMAX-NTMIN)/DT+1):
for i in range(100+1):
  #print NTMIN+DT*i,'%03d'%i
  #os.system('mv part_ang2_t'+str(NTMIN+DT*i)+'.png part_ang2_i'+('%03d'%i)+'.png')
  #os.system('mv sect2Dhr_fields_movie_t'+str(NTMIN+DT*i)+'.png sect2Dhr_fields_i'+('%03d'%i)+'.png')
  #print 'mv sect2Dhr_movie_t'+str(NTMIN+DT*i)+'.png xymap_fields_currents_i'+('%03d'%i)+'.png'
  #os.system('mv sect2Dhr_movie_t'+str(NTMIN+DT*i)+'.png xymap_fields_currents_i'+('%03d'%i)+'.png')
  #os.system('mv visit_B_EB_'+('%04d'%i)+'.png visit_B_EB_i'+('%04d'%i)+'.png')
  os.system('convert visit_B_EB_'+('%04d'%i)+'.png -crop +1+1 volume_B_EB_'+('%04d'%i)+'.png')

