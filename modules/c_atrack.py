#!/usr/bin/python3

import math
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt


##################################################################
class c_atrack:
  #
  def __init__(self):
    self.linear_length_scale = None
  #
  def load(self, f):
    ll = f.readline().strip().split(' ')
    self.track_size = int(ll[1])
    ll = f.readline().strip().split(' ')
    self.track_id = int(ll[1])
    f.readline() # ---
    f.readline() # i_frame x y
    # The data are in pix with y_inv.
    self.post_frame = []
    self.posx_px = []
    self.posy_px = []
    for l in f:
      l = l.strip()
      if len(l) == 0:  break
      ll = l.split('\t')
      self.post_frame.append( float(ll[0]) )
      self.posx_px.append( float(ll[1]) )
      self.posy_px.append( float(ll[2]) )
    self.n_pos = len(self.posx_px)
  #
  def set_im_params(self, um_per_pix, ms_per_frame, im_w_px, im_h_px):
    self.um_per_pix = um_per_pix
    self.ms_per_frame = ms_per_frame
    self.im_w_px = im_w_px
    self.im_h_px = im_h_px
    #
    self.s_per_frame = self.ms_per_frame / 1000.0
    self.im_w = self.im_w_px * um_per_pix
    self.im_h = self.im_h_px * um_per_pix
    self.im_center_x = self.im_w / 2.0
    self.im_center_y = self.im_h / 2.0
  #
  def pro1(self):
    self.post = []  # time relative to vid start, in seconds.
    self.posx = []
    self.posy = []
    for i in range(self.n_pos):
      self.post.append( self.post_frame[i] * self.s_per_frame )
      self.posx.append( self.posx_px[i] * self.um_per_pix )
      uposy = self.im_h_px - self.posy_px[i] - 1
      self.posy.append( uposy * self.um_per_pix )
    #
    self.post_last = self.post[self.n_pos-1]
    self.posx_last = self.posx[self.n_pos-1]
    self.posy_last = self.posy[self.n_pos-1]
    #
    self.delta_t = (self.n_pos-1) * self.s_per_frame
    self.delta_x = self.posx[ self.n_pos-1 ] - self.posx[0]
    self.delta_y = self.posy[ self.n_pos-1 ] - self.posy[0]
    self.mean_v_dx = self.delta_x / self.delta_t
    self.mean_v_dy = self.delta_y / self.delta_t
    #
    self.mean_v_mag2 = self.mean_v_dx**2 + self.mean_v_dy**2
    self.mean_v_mag  = math.sqrt( self.mean_v_mag2 )
    #
    self.mean_u_dx = self.mean_v_dx / self.mean_v_mag
    self.mean_u_dy = self.mean_v_dy / self.mean_v_mag
    #
    # The "sum_length" is the sum of each displacement.
    self.sum_length = 0.0
    for ib in range(1, self.n_pos):
      ia = ib-1
      dx = self.posx[ib] - self.posx[ia]
      dy = self.posy[ib] - self.posy[ia]
      d  = math.hypot(dx,dy)
      self.sum_length += d
    #
  #
  #
  def pro2(self):
    lls2 = self.linear_length_scale**2
    #
    # linpos(x y) is the original track using only points
    # that have traveled at least linear_length_scale from
    # the previous point.
    self.linposx = []
    self.linposy = []
    self.linposx.append( self.posx[0] )
    self.linposy.append( self.posy[0] )
    #
    pi0 = 0
    pi1 = 0
    for i in range(1, self.n_pos):
      pi1 = i
      p0x = self.posx[pi0]
      p0y = self.posy[pi0]
      p1x = self.posx[pi1]
      p1y = self.posy[pi1]
      delta2 = (p1x-p0x)**2 + (p1y-p0y)**2
      if delta2 >= lls2:
        self.linposx.append( p1x )
        self.linposy.append( p1y )
        pi0 = pi1
    self.n_linpos = len(self.linposx)
    #  print("n_linpos: ", self.n_linpos)
    #
    # displacement vectors.
    self.lin_dx = []
    self.lin_dy = []
    self.lin_vmag  = []
    for i in range(1, self.n_linpos):
      self.lin_dx.append( self.linposx[i] - self.linposx[i-1] )
      self.lin_dy.append( self.linposy[i] - self.linposy[i-1] )
      self.lin_vmag.append( math.sqrt( self.lin_dx[i-1]**2 + self.lin_dy[i-1]**2 ) )
    #
    self.n_lin_v = len(self.lin_dx)
    # curvatures for each set of two displacement vectors.
    self.curv = []
    for i in range(1, self.n_lin_v):
      im = i-1
      dotp = self.lin_dx[im] * self.lin_dx[i] + self.lin_dy[im] * self.lin_dy[i]
      dotpp = dotp / (self.lin_vmag[im] * self.lin_vmag[i])
      self.curv.append( math.acos( dotpp ) * self.linear_length_scale )
    #
    self.n_curv = len(self.curv)
    #
    self.mean_curv = 0.0
    for i in range(self.n_curv):
      self.mean_curv += self.curv[i]
    if self.n_curv == 0:
      self.mean_curv = float('nan')
    else:
      self.mean_curv /= self.n_curv
    #
  #
  def save_linear_data(self, oufname):
    ou = ''
    ou += 'i_lin_v curv\n'
    for i in range(self.n_curv):
      ou += str(i)
      ou += ' {0:0.3f}\n'.format(self.curv[i])
    fz = open(oufname, 'w')
    fz.write(ou)
    fz.close()
  #
  def plot_mean_v(self):
    p0 = [0, self.mean_v_dx]
    p1 = [0, self.mean_v_dy]
    plt.plot(p0, p1, color='#333333')
  #
  def plot_track(self, color=None):
    if color == None:
      plt.plot(self.posx, self.posy)
    else:
      plt.plot(self.posx, self.posy,
        color=color
        )
  #
  def plot_track_lin(self, color=None):
    if color == None:
      plt.plot(self.linposx, self.linposy)
    else:
      plt.plot(self.linposx, self.linposy,
        color=color
        )
  #
  #
##################################################################



