#!/usr/bin/python3

from modules.c_asti_trackpy_conf import c_asti_trackpy_conf
from modules.c_atrack import c_atrack

import math
import sys
from matplotlib import pyplot as plt




fname_conf = sys.argv[1]

############################################
f = open( fname_conf )
for l in f:
  if not l.startswith('!'):  continue
  l = l.strip()
  ll = l.split(' ')
  key = ll[0]
  ###
  if key == '!fname_asti_trackpy_conf':  fname_asti_trackpy_conf = ll[1]
  elif key == '!dir_asti_tp':  dir_asti_tp = ll[1]
  elif key == '!oudir':  oudir = ll[1]
  elif key == '!oufname1':  oufname1 = ll[1]
  elif key == '!ougfname1':  ougfname1 = ll[1]
  elif key == '!ougfname2':  ougfname2 = ll[1]
  elif key == '!linear_length_scale':  linear_length_scale = float(ll[1])
  else:
    print("Error.  Unrecognized key.")
    print("  key: ", key)
    sys.exit(1)
f.close()
############################################


atp_conf = c_asti_trackpy_conf()
atp_conf.load( dir_asti_tp+'/'+fname_asti_trackpy_conf )


print("p size: ", atp_conf.particle_size)


atrack = []
f = open( dir_asti_tp+'/'+atp_conf.fname_out1 )

n_track = int( f.readline().strip().split(' ')[1] )
for i in range(n_track):  atrack.append( c_atrack() )

l = f.readline().strip()  # track sizes.
ll = l.split(' ')
ts = []
for i in range(1,len(ll)):  ts.append( int(ll[i]) )
if len(ts) != n_track:
  print("Error.  len(ts) != n_track.")
  sys.exit(1)

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
  atrack[i].load(f)
f.close()

for i in range(n_track):
  if atrack[i].n_pos != ts[i]:
    print("Error.")
    print("  atrack[i].n_pos != ts[i].")
    print("  i:  ", i)
    sys.exit(1)


for i in range(n_track):
  atrack[i].set_im_params(
    atp_conf.um_per_pix,
    atp_conf.ms_per_frame,
    atp_conf.im_w,
    atp_conf.im_h
    )

for i in range(n_track):
  atrack[i].pro1()

for i in range(n_track):
  atrack[i].linear_length_scale = linear_length_scale
  atrack[i].pro2()


ou = ''
ou += 'i_track mean_u_dx(um/s) mean_u_dy(um/s) mean_u(um/s)\n'
for i in range(n_track):
  ou += str(i)
  ou += ' {0:0.3f}'.format( atrack[i].mean_u_dx )
  ou += ' {0:0.3f}'.format( atrack[i].mean_u_dy )
  ou += ' {0:0.3f}'.format( atrack[i].mean_u )
  ou += '\n'
fz = open(oudir+'/'+oufname1, 'w')
fz.write(ou)
fz.close()


mean_u_max  = atrack[0].mean_u


for i in range(1, n_track):
  if atrack[i].mean_u > mean_u_max:
    mean_u_max = atrack[i].mean_u


pos0_x = []
pos0_y = []
for i in range(n_track):
  pos0_x.append( atrack[i].posx[0] )
  pos0_y.append( atrack[i].posy[0] )


##################################################################
fig = plt.figure()

plt.plot( pos0_x, pos0_y,
  linestyle='none',
  marker='o',
  markeredgecolor='#000000',
  markerfacecolor='none',
  markersize=8
  )

for i in range(n_track):
  atrack[i].plot_track()

plt.xlim(-10, atrack[0].im_w+10 )
plt.ylim(-10, atrack[0].im_h+10 )
plt.gca().set_aspect('equal', adjustable='box')

plt.title("scale:  um")

plt.savefig(oudir+'/'+ougfname1)



##################################################################
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
  if r > mean_u_max:  break
  for i in range(n_circ_pnt):
    ang = i * dang
    circx.append( r * math.cos(ang) )
    circy.append( r * math.sin(ang) )
  circx.append(None)
  circy.append(None)

axex1 = [-mean_u_max, mean_u_max, None, 0, 0]
axey1 = [0, 0, None, -mean_u_max, mean_u_max]
plt.plot( axex1, axey1, color="#dddddd" )
plt.plot( circx, circy, color="#dddddd" )

for i in range(n_track):
  atrack[i].plot_mean_u()

plt.xlim( -mean_u_max-10, mean_u_max+10 )
plt.ylim( -mean_u_max-10, mean_u_max+10 )
plt.gca().set_aspect('equal', adjustable='box')

plt.title("scale:  um/s")

plt.savefig(oudir+'/'+ougfname2)






