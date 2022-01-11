#!/usr/bin/python3

from modules.c_asti_trackpy_conf import c_asti_trackpy_conf

import sys




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
  else:
    print("Error.  Unrecognized key.")
    print("  key: ", key)
    sys.exit(1)
f.close()
############################################


atp_conf = c_asti_trackpy_conf()
atp_conf.load( fname_asti_trackpy_conf )


print("p size: ", atp_conf.particle_size)




