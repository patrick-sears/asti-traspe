#!/usr/bin/python3

from matplotlib import pyplot as plt
import math


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
    self.posx_px = []
    self.posy_px = []
    for l in f:
      l = l.strip()
      if len(l) == 0:  break
      ll = l.split('\t')
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
  #
  def pro1(self):
    self.posx = []
    self.posy = []
    for i in range(self.n_pos):
      self.posx.append( self.posx_px[i] * self.um_per_pix )
      uposy = self.im_h_px - self.posy_px[i] - 1
      self.posy.append( uposy * self.um_per_pix )
  #
    self.delta_t = (self.n_pos-1) * self.s_per_frame
    self.delta_x = self.posx[ self.n_pos-1 ] - self.posx[0]
    self.delta_y = self.posy[ self.n_pos-1 ] - self.posy[0]
    self.mean_u_dx = self.delta_x / self.delta_t
    self.mean_u_dy = self.delta_y / self.delta_t
    #
    self.mean_u2 = self.mean_u_dx**2 + self.mean_u_dy**2
    self.mean_u  = math.sqrt( self.mean_u2 )
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
  def plot_mean_u(self):
    p0 = [0, self.mean_u_dx]
    p1 = [0, self.mean_u_dy]
    plt.plot(p0, p1)
  #
  def plot_track(self):
    plt.plot(self.posx, self.posy)
  #
  #
  #
##################################################################



