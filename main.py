#!/usr/bin/python3

from modules.c_asti_trackpy_conf import c_asti_trackpy_conf
from modules.c_atrack import c_atrack

import math
import sys
import os
from matplotlib import pyplot as plt
from datetime import datetime

stime_hu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


fname_conf = sys.argv[1]



######################
def read_expected_v_ang(val_type, val_str):
  #
  if val_type == 'math_deg':
    ang1 = float(val_str)
    ang = ang1 * math.pi / 180.0
  elif val_type == 'geo_deg':
    ang1 = float(val_str)
    ang = (90.0 - ang1) * math.pi / 180.0
  elif val_type == 'geo_name':
    dict = {  'N':0,   'NE':45,  'E':90,  'SE':135,
              'S':180, 'NW':-45, 'W':-90, 'SW':-135 }
    ang1 = dict[val_str]
    ang = (90.0 - ang1) * math.pi / 180.0
  else:
    print("Error in read_expected_v_ang.")
    print("  val_type: ", val_type)
    print("  val_str:  ", val_str)
    sys.exit(1)
  #
  ux = math.cos( ang )
  uy = math.sin( ang )
  return ux, uy
######################




exou_id = []

############################################
# Read the asti-trapse config file.
f = open( fname_conf )
for l in f:
  if not l.startswith('!'):  continue
  l = l.strip()
  ll = l.split(' ')
  key = ll[0]
  ###
  if key == '!run_name':
    run_name = ll[1]
    print("run_name: ", run_name)
  elif key == '!fname_asti_trackpy_conf':  fname_asti_trackpy_conf = ll[1]
  elif key == '!dir_asti_tp':  dir_asti_tp = ll[1]
  elif key == '!oudir':  oudir = ll[1]
  elif key == '!oufname1':  oufname1 = ll[1]
  elif key == '!oufname2':  oufname2 = ll[1]
  elif key == '!oufname_s1':  oufname_s1 = ll[1]  # s#:  sum files
  elif key == '!oufname_g1':  oufname_g1 = ll[1]
  elif key == '!oufname_g2':  oufname_g2 = ll[1]
  elif key == '!oufname_g3':  oufname_g3 = ll[1]
  elif key == '!linear_length_scale':  linear_length_scale = float(ll[1])
  elif key == '!exou_dir':  exou_dir = ll[1]
  elif key == '!use_expected_v_ang':
    if ll[1] == '1':  use_expected_v_ang = True
    else:             use_expected_v_ang = False
  elif key == '!expected_v_ang':
    expected_ux, expected_uy = read_expected_v_ang( ll[1], ll[2] )
  elif key == '!use_exou':
    n_exou = 0
    if ll[1] == '1':  use_exou = True
    else:             use_exou = False
  elif key == '!exou_id':
    for l in f:
      l = l.strip()
      if len(l) == 0:  break
      if l[0] == '#':  continue
      lu = l.split('#')
      ll = lu[0].strip().split(' ')
      for val_str in ll:
        exou_id.append( int(val_str) )
    n_exou = len(exou_id)
  else:
    print("Error.  Unrecognized key.")
    print("  key: ", key)
    sys.exit(1)
f.close()
############################################



#################################
# Read the asti-trackpy config file.
atp_conf = c_asti_trackpy_conf()
atp_conf.load( dir_asti_tp+'/'+fname_asti_trackpy_conf )
#################################



###################### fff
# Open the log file and write some initial stuff.
flog = open(oudir+'/'+oufname2, 'w')
flog.write("Run time: "+stime_hu+'\n')
flog.write("Run name: "+run_name+'\n')
flog.write('\n')

flog.write('\nparticle_size: '+str(atp_conf.particle_size)+'\n')

fou = ''
if use_expected_v_ang:
  fou += 'expected ux uy:'
  fou += ' {0:0.3f}'.format(expected_ux)
  fou += ' {0:0.3f}'.format(expected_uy)
else:
  fou += 'expected ux uy:'
  fou += '  not_used not_used'
fou += '\n'

fou += 'particle_size: '+str(atp_conf.particle_size)+'\n'
flog.write(fou)
###################### fff







############################################ <***>
# Create atrack[], read asti-trackpy data, and fill atrack[].
print("Reading asti-trackpy data.")
#
atrack = []
f = open( dir_asti_tp+'/'+atp_conf.fname_out1 )
n_track = int( f.readline().strip().split(' ')[1] )
print("n_track: ", n_track)
flog.write("n_track: "+str(n_track)+'\n')
for i in range(n_track):
  print(".", end='', flush=True)
  atrack.append( c_atrack() )
print()
#
l = f.readline().strip()  # read track sizes.
ll = l.split(' ')
ts = []
for i in range(1,len(ll)):  ts.append( int(ll[i]) )
if len(ts) != n_track:
  print("Error.  len(ts) != n_track.")
  sys.exit(1)
#
i = -1
for l in f:
  if not l.startswith('!'):  continue
  i += 1
  ll = l.split(' ')
  i_track = int(ll[2])
  if i_track != i:
    print("Error.  i_track != i.")
    print("  i:       ", i)
    print("  i_track: ", i_track)
    sys.exit(0)
  # atrack[i] reads its asti-trackpy data from file.
  atrack[i].load(f)
#
#  Done reading asti-trackpy file.
f.close()
############################################ <***>




#################################
# Record track IDs to log file.
fou = ''
fou += 'Track IDs (track_id):'  # no \n here
n_ret = 0
for i in range(n_track):
  if n_ret == 0:  fou += '\n  '
  # fou += ' '+str(atrack[i].track_id)
  fou += ' {0:4d}'.format(atrack[i].track_id)
  n_ret += 1
  if n_ret == 10:  n_ret = 0
fou += '\n'
flog.write(fou)
#################################




######################
# Check to make sure the number of particle positions
# for each track from the start of the asti-trackpy file
# matches the number of positions each atrack[i] actually
# loaded.
for i in range(n_track):
  if atrack[i].n_pos != ts[i]:
    print("Error.")
    print("  atrack[i].n_pos != ts[i].")
    print("  i:  ", i)
    sys.exit(1)
######################




############################################ ^^^
# Create exou output dirs.
if use_exou:
  exou_i = []
  exou_tdir = [] # track dir
  for i in range(n_exou):
    exou_i.append( None )
    exou_tdir.append ( exou_dir+'/{0:04d}'.format( exou_id[i] ) )
    if not os.path.exists( exou_tdir[i] ):
      os.mkdir( exou_tdir[i] )
    #
    found = False
    for j in range(n_track):
      if exou_id[i] == atrack[j].track_id:
        found = True
        exou_i[i] = j
        break
    if not found:
      print("Error.")
      print("  An exou_id was not found.")
      print("  exou_id: ", exou_id)
      sys.exit(1)
############################################ ^^^


#################################
# Copy asti-tackpy settings to each atrack[i].
for i in range(n_track):
  atrack[i].set_im_params(
    atp_conf.um_per_pix,
    atp_conf.ms_per_frame,
    atp_conf.im_w,
    atp_conf.im_h
    )
#################################




################################# <===>
# Run the atrack processing functions.
for i in range(n_track):
  atrack[i].pro1()

for i in range(n_track):
  atrack[i].linear_length_scale = linear_length_scale
  atrack[i].pro2()

if use_exou:
  for ix in range(n_exou):
    it = exou_i[ix]
    oufname = exou_tdir[ix]+'/linear.data'
    atrack[it].save_linear_data( oufname )
################################# <===>



################################# ccc
# xxx
################################# ccc




############################################
# Save oufname1 data.
ou = ''
ou += 'Column long headings:\n'
ou += '  i id:  i_track track_id\n'
ou += '  dx dy:  mean_v_dx(um/s) mean_v_dy(um/s)\n'
ou += '  v_mag:  mean_v_mag(um/s)\n'
ou += '  curv:   mean_curv(um^-1)\n'
ou += '------------------------------------------\n'
ou += 'i   id   dx       dy       v_mag   curv\n'
ou += '--- ---- -------- -------- ------- -------\n'
for i in range(n_track):
  ou += '{0:3d}'.format(i)
  ou += ' {0:4d}'.format(atrack[i].track_id)
  #
  ou += ' {0:8.3f}'.format( atrack[i].mean_v_dx )
  ou += ' {0:8.3f}'.format( atrack[i].mean_v_dy )
  ou += ' {0:7.3f}'.format( atrack[i].mean_v_mag )
  #
  ou += ' {0:7.3f}'.format( atrack[i].mean_curv )
  ou += '\n'
fz = open(oudir+'/'+oufname1, 'w')
fz.write(ou)
fz.close()
############################################



################################# ---
# Find the maximum velocity.
# For graphing.
mean_v_max  = atrack[0].mean_v_mag
for i in range(1, n_track):
  if atrack[i].mean_v_mag > mean_v_max:
    mean_v_max = atrack[i].mean_v_mag
################################# ---



######################
# Record the first position for each track.
# This is only for graphing tacks and marking
# where they start.
pos0_x = []
pos0_y = []
for i in range(n_track):
  pos0_x.append( atrack[i].posx[0] )
  pos0_y.append( atrack[i].posy[0] )
######################


###########
# print("n_exou: ", n_exou)
# Can be left like this even if use_exou == False.
flog.write("n_exou: "+str(n_exou)+'\n')
fou = ''
for i in range(n_exou):
  fou += '  track_id {0:04d}\n'.format( exou_id[i] )
flog.write(fou)
###########




###########
# Calculate the length of all particle tracks, end to end.
# This will be used to weight some means of per-track
# measurements.
all_track_sum_length = 0.0
for i in range(n_track):
  all_track_sum_length += atrack[i].sum_length
###########




############################################ &&&
# Calculate ats data.
# ats:  all track summary
ats_mean_v_dx = 0.0
ats_mean_v_dy = 0.0
for i in range(n_track):
  ats_mean_v_dx += atrack[i].mean_v_dx
  ats_mean_v_dy += atrack[i].mean_v_dy
ats_mean_v_dx /= n_track
ats_mean_v_dy /= n_track
ats_mean_v_mag = math.hypot(ats_mean_v_dx, ats_mean_v_dy)
ats_mean_u_dx = ats_mean_v_dx / ats_mean_v_mag
ats_mean_u_dy = ats_mean_v_dy / ats_mean_v_mag
ats_mean_u_mag = math.hypot(ats_mean_u_dx, ats_mean_u_dy)
# ats_mean_u_mag should be 1.000.
# I'm still outputting it to the file as both a check and a
# reminder.
#
# The ats_mean_curv will be weighted by track length.
# One reason to do this is that some tracks get cut
# into many smaller tracks.  This happens if trackpy
# has trouble seeing the particles.
ats_wmean_curv = 0.0
for i in range(n_track):
  ats_wmean_curv += atrack[i].mean_curv * atrack[i].sum_length
ats_wmean_curv /= all_track_sum_length
#
# Calculate how well aligned the tracks are independent
# of the speed.  I.e. the mean of the unit vectors.
# It is the "alignment vector".  Note it is not a unit
# vector.
ats_v_align_dx = 0.0
ats_v_align_dy = 0.0
ats_v_align_mag = 0.0
for i in range(n_track):
  ats_v_align_dx += atrack[i].mean_u_dx
  ats_v_align_dy += atrack[i].mean_u_dy
ats_v_align_dx /= n_track
ats_v_align_dy /= n_track
ats_v_align_mag = math.hypot( ats_v_align_dx, ats_v_align_dy )
#
# Get the mean speed.
# As usual for mean values, it's from the first track point
# to the last.  Unlike ats_mean_v_mag, it ignores the relative
# directions of the tracks.  The values of ats_mean_v_mag
# and ats_mean_speed should be the same if the tracks are
# perfectly aligned (ats_v_align_mag == 1).
ats_mean_speed = 0.0
for i in range(n_track):
  ats_mean_speed += atrack[i].mean_v_mag
ats_mean_speed /= n_track
#
############################################ &&&



############################################
# Save ats data (summary data).
ou = ''
ou += 'n_track: '+str(n_track)+'\n'
ou += '\n'
ou += 'ats_mean_v_dx (um/s):    {0:8.3f}\n'.format(ats_mean_v_dx)
ou += 'ats_mean_v_dy (um/s):    {0:8.3f}\n'.format(ats_mean_v_dy)
ou += 'ats_mean_v_mag (um/s):   {0:8.3f}\n'.format(ats_mean_v_mag)
ou += 'ats_mean_speed (um/s):   {0:8.3f}\n'.format(ats_mean_speed)
ou += 'ats_mean_u_dx (um/s):    {0:8.3f}\n'.format(ats_mean_u_dx)
ou += 'ats_mean_u_dy (um/s):    {0:8.3f}\n'.format(ats_mean_u_dy)
ou += 'ats_mean_u_mag (um/s):   {0:8.3f}\n'.format(ats_mean_u_mag)
ou += 'ats_v_align_mag (1):     {0:8.3f}\n'.format(ats_v_align_mag)
ou += 'ats_wmean_curv (um^-1):  {0:8.3f}\n'.format(ats_wmean_curv)
ou += '\n\n'
#
fz = open(oudir+'/'+oufname_s1, 'w')
fz.write(ou)
fz.close()
############################################





##################################################################
### !graph #######################################################
# The tracks.
fig = plt.figure()

plt.plot( pos0_x, pos0_y,
  linestyle='none',
  marker='o',
  markeredgecolor='#000000',
  markerfacecolor='none',
  markersize=8
  )

ca = fig.gca()

for i in range(n_track):
  atrack[i].plot_track()
  ca.annotate( str(atrack[i].track_id),
    xy = (atrack[i].posx[0]+5, atrack[i].posy[0]-5)
    )


plt.xlim(-10, atrack[0].im_w+10 )
plt.ylim(-10, atrack[0].im_h+10 )
plt.gca().set_aspect('equal', adjustable='box')

plt.title("scale:  um")

plt.savefig(oudir+'/'+oufname_g1)











##################################################################
### !graph #######################################################
# The velocity vectors.
plt.clf()
fig = plt.figure()

n_circ_seg = 80
n_circ_pnt = n_circ_seg + 1
dang = math.pi * 2.0 / n_circ_seg
circx = []
circy = []
r = 0.0
while True:
  r += 50.0
  if r > mean_v_max:  break
  for i in range(n_circ_pnt):
    ang = i * dang
    circx.append( r * math.cos(ang) )
    circy.append( r * math.sin(ang) )
  circx.append(None)
  circy.append(None)

axex1 = [-mean_v_max, mean_v_max, None, 0, 0]
axey1 = [0, 0, None, -mean_v_max, mean_v_max]
plt.plot( axex1, axey1, color="#dddddd" )
plt.plot( circx, circy, color="#dddddd" )

if use_expected_v_ang:
  gra_expect_ux = [0, mean_v_max * expected_ux]
  gra_expect_uy = [0, mean_v_max * expected_uy]
  plt.plot(gra_expect_ux, gra_expect_uy,
    color='#aaffaa',
    linewidth=3.0
    )

for i in range(n_track):
  atrack[i].plot_mean_v()


gra_mean_v_x = [0, ats_mean_v_dx]
gra_mean_v_y = [0, ats_mean_v_dy]
plt.plot(gra_mean_v_x, gra_mean_v_y,
  color='#ff0000',
  linewidth=3.0
  )


plt.xlim( -mean_v_max-10, mean_v_max+10 )
plt.ylim( -mean_v_max-10, mean_v_max+10 )
plt.gca().set_aspect('equal', adjustable='box')

plt.title("scale:  um/s")

plt.savefig(oudir+'/'+oufname_g2)





##################################################################
### !graph #######################################################
# The linearized tracks.
plt.clf()
fig = plt.figure()

plt.plot( pos0_x, pos0_y,
  linestyle='none',
  marker='o',
  markeredgecolor='#000000',
  markerfacecolor='none',
  markersize=8
  )

ca = fig.gca()

for i in range(n_track):
  atrack[i].plot_track_lin()
  ca.annotate( str(atrack[i].track_id),
    xy = (atrack[i].posx[0]+5, atrack[i].posy[0]-5)
    )


plt.xlim(-10, atrack[0].im_w+10 )
plt.ylim(-10, atrack[0].im_h+10 )
plt.gca().set_aspect('equal', adjustable='box')

plt.title("scale:  um")

plt.savefig(oudir+'/'+oufname_g3)









##################################################################
### !graph #######################################################
# The exou tracks.
if use_exou:
  ################### ggg
  for xi in range(n_exou):
    i = exou_i[xi]
    #
    plt.clf()
    fig = plt.figure()
    #
    plt.plot( [pos0_x[i]], [pos0_y[i]],
      linestyle='none',
      marker='o',
      markeredgecolor='#000000',
      markerfacecolor='none',
      markersize=8
      )
    #
    ca = fig.gca()
    #
    for j in range(n_track):
      if j == i:  continue
      atrack[j].plot_track(color='#cccccc')
    #
    # Plot the track of interest on top.
    atrack[i].plot_track(color='#990000')
    #
    plt.xlim(-10, atrack[0].im_w+10 )
    plt.ylim(-10, atrack[0].im_h+10 )
    plt.gca().set_aspect('equal', adjustable='box')
    #
    title = "track_id "+str(exou_id[xi])+", scale: um."
    plt.title(title)
    #
    oufname = exou_tdir[xi]+'/track.png'
    # print("saving:  ", oufname)
    plt.savefig(oufname)
  ################### ggg



##################################################################
### !graph #######################################################
# The exou linearised tracks.
if use_exou:
  ################### ggg
  for xi in range(n_exou):
    i = exou_i[xi]
    #
    plt.clf()
    fig = plt.figure()
    #
    plt.plot( [pos0_x[i]], [pos0_y[i]],
      linestyle='none',
      marker='o',
      markeredgecolor='#000000',
      markerfacecolor='none',
      markersize=8
      )
    #
    ca = fig.gca()
    #
    for j in range(n_track):
      if j == i:  continue
      atrack[j].plot_track_lin(color='#cccccc')
    #
    # Plot the track of interest on top.
    atrack[i].plot_track_lin(color='#990000')
    #
    plt.xlim(-10, atrack[0].im_w+10 )
    plt.ylim(-10, atrack[0].im_h+10 )
    plt.gca().set_aspect('equal', adjustable='box')
    #
    title = "track_id "+str(exou_id[xi])+", scale: um."
    plt.title(title)
    #
    oufname = exou_tdir[xi]+'/track_linear.png'
    # print("saving:  ", oufname)
    plt.savefig(oufname)
  ################### ggg




##################################################################
### !graph #######################################################
# End of graphs.
##################################################################



