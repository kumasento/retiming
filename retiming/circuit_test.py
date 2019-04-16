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


if __name__ == '__main__':
  unittest.main()