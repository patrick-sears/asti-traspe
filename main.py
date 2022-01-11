#!/usr/bin/python3

import sys

fname_conf = sys.argv[1]

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


############################################ **config
f = open(fname_asti_trackpy_conf)
for l in f:
  if not l.startswith('!'):  continue
  l = l.strip()
  ll = l.split(' ')
  key = ll[0]
  if key == '!imdir':
    if len(ll) == 2:    imdir = ll[1]
    else:               imdir = f_config.readline().strip()
  elif key == '!um_per_pix':
    um_per_pix = float(ll[1])
  elif key == '!ms_per_frame':
    ms_per_frame = float(ll[1])
  elif key == '!fname_out1':
    fname_out1 = ll[1]
  elif key == '!fname_out2':
    fname_out2 = ll[1]
  elif key == '!track_ims_dir':
    track_ims_dir = ll[1]
  elif key == '!track_ims_vidname':
    track_ims_vidname = ll[1]
  #
  elif key == '!imfile_basename':
    imfile_basename = ll[1]
  elif key == '!imfile_suffix':
    imfile_suffix = ll[1]
  elif key == '!imfile_i_first':
    imfile_i_first = int(ll[1])
  elif key == '!imfile_i_last':
    imfile_i_last = int(ll[1])
  elif key == '!imfile_digs':
    imfile_digs = int(ll[1])
  #
  elif key == '!im_w':
    im_w = int(ll[1])
  elif key == '!im_h':
    im_h = int(ll[1])
  #
  elif key == '!min_frames_in_a_track':
    min_frames_in_a_track = int(ll[1])
  #
  elif key == '!particle_size':
    particle_size = float(ll[1])
  elif key == '!search_range':
    search_range = float(ll[1])
  elif key == '!tpl_minmass':
    tpl_minmass = int(ll[1])
  elif key == '!min_track_len_px':
    min_track_len_px = float(ll[1])
  #
  elif key == '!sup01_f2name':  continue
  elif key == '!sup01_f3name':  continue
  elif key == '!sup01_f4name':  continue
  else:
    print("Error.  Unrecognized key.")
    print("  key = ", key)
    exit(1)
f.close()
############################################ **config



