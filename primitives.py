class Node(object):
  def __init__(self, coordinates : list):
    self.x = coordinates[0];
    self.y = coordinates[1];
    self.z = coordinates[2];
  def __str__(self):
    return f"x = {self.x}|y ={self.y}|z = {self.z}"
