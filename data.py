from primitives import *
import copy 
import numpy as np

def move_z(x: Node):
  tmp = np.identity(4)
  tmp[:-1,-1] = np.array([0,0, -80])
  x.coordinates = tmp @ x.coordinates
  return x

def flip_x(x):
  tmp = np.identity(4)
  tmp[0,0] = -1
  x.coordinates = tmp @ x.coordinates
  return x

def init() -> List[Type[Node]] :
  ### BEGIN SQUARE
  n0 = Node([10, -25, 50, 1])
  n1 = Node([50, -25, 50, 1])
  n2 = Node([50, 25, 50, 1])
  n3 = Node([10, 25, 50, 1])

  e0_1 = Edge(n0, n1)
  e1_2 = Edge(n1, n2)
  e2_3 = Edge(n2, n3)
  e3_0 = Edge(n3, n0)

  n4 = Node([10, -25, 75, 1])
  n5 = Node([50, -25, 75, 1])
  n6 = Node([50, 25, 75, 1])
  n7 = Node([10, 25, 75, 1])

  e4_5 = Edge(n4, n5)
  e5_6 = Edge(n5, n6)
  e6_7 = Edge(n6, n7)
  e7_4 = Edge(n7, n4)

  e0_4 = Edge(n0, n4)
  e1_5 = Edge(n1, n5)
  e2_6 = Edge(n2, n6)
  e3_7 = Edge(n3, n7)

  data = [n0, n1, n2, n3, n4, n5, n6, n7]
  edges = [e0_1, e1_2, e2_3, e3_0, e4_5, e5_6, e6_7, e7_4, e0_4, e1_5, e2_6, e3_7]


  square = WorldObject()
  square.add_edges(edges)
  square.add_nodes(data)

  s1 : WorldObject= copy.deepcopy(square)
  list(map(move_z, s1.nodes))
  s2 = copy.deepcopy(s1)
  s3 = copy.deepcopy(square)

  list(map(flip_x, s2.nodes))
  list(map(flip_x, s3.nodes))

  r0 = Node([5, -25, 75, 1])
  r1 = Node([5, -25, -75, 1])
  r2 = Node([-5, -25, -75, 1])
  r3 = Node([-5, -25, 75, 1])

  er0_1 = Edge(r0,r1)
  er1_2 = Edge(r1,r2)
  er2_3 = Edge(r2,r3)
  er3_0 = Edge(r3,r0)
  road = [er0_1, er1_2, er2_3, er3_0 ]
  return square.edges + s1.edges + s2.edges + s3.edges + road 