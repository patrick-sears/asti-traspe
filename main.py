#!/usr/bin/python3

from modules.c_asti_trackpy_conf import c_asti_trackpy_conf
from modules.c_atrack import c_atrack


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






##################################################################
fig = plt.figure()

for i in range(n_track):
  atrack[i].draw_track()

plt.savefig('z005.png')



