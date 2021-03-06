from typing import Type, List
import numpy as np
import copy


class Node(object):
    def __init__(self, coordinates: list):
        self.coordinates = np.array(coordinates)

    def __repr__(self):
        return f"coordinates = {self.coordinates}"

    def __str__(self):
        return f"coordinates = {self.coordinates}"


class Edge(object):
    def __init__(self, begin: Type[Node], end: Type[Node]):
        self.begin = begin
        self.end = end

    def __str__(self):
        return f"begin = ({self.begin}), end = ({self.end})"


class Triangle(object):
    def __init__(self, one, two, tree, colour=(0, 255, 0), name="NoName"):
        self.one = copy.deepcopy(one)
        self.two = copy.deepcopy(two)
        self.tree = copy.deepcopy(tree)
        self.no = [self.one, self.two, self.tree]
        self.colour = colour
        self.name = name

    def setColour(self, colour):
        self.colour = colour

    def nodes(self):
        return self.no

    def __str__(self):
        return f"{self.no}"


class WorldObject(object):
    def __init__(self):
        self.nodes: list = []
        self.edges: list = []

    def add_nodes(self, nodes: List[Type[Node]]):
        for node in nodes:
            self.nodes.append(node)

    def add_edges(self, edges: List[Type[Edge]]):
        for edge in edges:
            self.edges.append(edge)

    def print_nodes(self):
        print(self.nodes[:])

    def print_edges(self):
        print(self.edges[:])
