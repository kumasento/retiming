""" Test circuit.py """

import unittest
import networkx as nx

from retiming import circuit as ct


class CircuitTest(unittest.TestCase):

  def test_create_graph(self):
    G = ct.create_graph()
    self.assertIsInstance(G, nx.MultiDiGraph)

  def test_add_register(self):
    G = ct.create_graph()
    R1 = ct.add_register(G)
    R2 = ct.add_register(G)

    self.assertEqual(R1, 'R1')
    self.assertEqual(R2, 'R2')

  def test_get_registers(self):
    G = ct.create_graph()
    R1 = ct.add_register(G)
    R2 = ct.add_register(G)
    self.assertListEqual(ct.get_registers(G), ['R1', 'R2'])

  def test_add_vertex(self):
    G = ct.create_graph()

    V1 = ct.add_vertex(G, 1)
    self.assertEqual(V1, 'V1')

    # delay should be nonnegative
    with self.assertRaises(AssertionError):
      ct.add_vertex(G, -1)

  def test_add_edge(self):
    G = ct.create_graph()
    R = ct.add_register(G)
    V1 = ct.add_vertex(G, 2)
    V2 = ct.add_vertex(G, 2)

    # edge from V1 to R, R to V2
    ct.add_edge(G, V1, R)
    ct.add_edge(G, R, V2)

    self.assertEqual(len(G.nodes()), 3)
    self.assertEqual(len(G.edges()), 2)

    with self.assertRaises(ValueError):
      ct.add_edge(G, 'p', 'q')


if __name__ == '__main__':
  unittest.main()