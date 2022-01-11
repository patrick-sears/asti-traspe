#!/usr/bin/python3



##################################################################
class c_asti_trackpy_conf:
  #
  def __init__(self):
    self.fname = None
  #
  def load(self, fname):
    self.fname = fname
    f = open(fname)
    #####################
    for l in f:
      if not l.startswith('!'):  continue
      l = l.strip()
      ll = l.split(' ')
      key = ll[0]
      if key == '!imdir':
        if len(ll) == 2:    self.imdir = ll[1]
        else:               self.imdir = f_config.readline().strip()
      elif key == '!um_per_pix':
        self.um_per_pix = float(ll[1])
      elif key == '!ms_per_frame':
        self.ms_per_frame = float(ll[1])
      elif key == '!fname_out1':
        self.fname_out1 = ll[1]
      elif key == '!fname_out2':
        self.fname_out2 = ll[1]
      elif key == '!track_ims_dir':
        self.track_ims_dir = ll[1]
      elif key == '!track_ims_vidname':
        self.track_ims_vidname = ll[1]
      #
      elif key == '!imfile_basename':
        self.imfile_basename = ll[1]
      elif key == '!imfile_suffix':
        self.imfile_suffix = ll[1]
      elif key == '!imfile_i_first':
        self.imfile_i_first = int(ll[1])
      elif key == '!imfile_i_last':
        self.imfile_i_last = int(ll[1])
      elif key == '!imfile_digs':
        self.imfile_digs = int(ll[1])
      #
      elif key == '!im_w':
        self.im_w = int(ll[1])
      elif key == '!im_h':
        self.im_h = int(ll[1])
      #
      elif key == '!min_frames_in_a_track':
        self.min_frames_in_a_track = int(ll[1])
      #
      elif key == '!particle_size':
        self.particle_size = float(ll[1])
      elif key == '!search_range':
        self.search_range = float(ll[1])
      elif key == '!tpl_minmass':
        self.tpl_minmass = int(ll[1])
      elif key == '!min_track_len_px':
        self.min_track_len_px = float(ll[1])
      #
      elif key == '!sup01_f2name':  continue
      elif key == '!sup01_f3name':  continue
      elif key == '!sup01_f4name':  continue
      else:
        print("Error reading config.")
        print("  fname: ", self.fname)
        print("  Unrecognized key.")
        print("  key = ", key)
        exit(1)
    #####################
    f.close()
  #
  #
  #
##################################################################





