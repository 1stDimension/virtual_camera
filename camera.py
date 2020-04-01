import numpy as np

class Camera(object):
  def __init__(self, position, gaze, view_up):
    self.position = position
    self.gaze = gaze
    self.view_up = view_up

    self.w = -1 * gaze / np.linalg.norm(gaze)
    cross = np.cross(view_up, self.w)
    self.u = cross / np.linalg.norm(cross) 
    self.v = np.cross(self.w,self.u)
    
    self.rotation = np.identity(4)
    self.rotation[0,:-1] = self.u
    self.rotation[1,:-1] = self.v
    self.rotation[2,:-1] = self.w

    self.transform = np.identity(4)
    self.transform[:-1,-1] = -position