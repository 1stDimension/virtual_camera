from typing import Type, List

class Node(object):
  def __init__(self, coordinates : list):
    self.x = coordinates[0];
    self.y = coordinates[1];
    self.z = coordinates[2];
  def __str__(self):
    return f"x = {self.x}|y ={self.y}|z = {self.z}"

class Edge(object):
  def __init__(self, begin : Type[Node], end: Type[Node]):
    self.begin = begin
    self.end = end
  def __str__(self):
    return f"begin = ({self.begin}), end = ({self.end})"

class WorldObject(object):
  def __init__(self):
    self.nodes : list = []
    self.edges : list = []
  
  def add_nodes(self, nodes : List[Type[Node]]):
    for node in nodes:
      self.nodes.append(node)

  def add_edges(self, edges : List[Type[Edge]]):
    for edge in edges:
      self.edges.append(edge)

