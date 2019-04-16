""" Test circuit.py """

import unittest
import networkx as nx

from retiming import circuit as ct


class CircuitTest(unittest.TestCase):

  def test_create_graph(self):
    G = ct.create_graph()
    self.assertIsInstance(G, nx.MultiDiGraph)

  def test_add_vertex(self):
    G = ct.create_graph()

    V1 = ct.add_vertex(G, 1)
    self.assertEqual(V1, 'V1')
    self.assertEqual(G.node[V1]['weight'], 1)

    # delay should be nonnegative
    with self.assertRaises(AssertionError):
      ct.add_vertex(G, -1)

  def test_add_edge(self):
    G = ct.create_graph()
    V1 = ct.add_vertex(G, 2)
    V2 = ct.add_vertex(G, 2)

    # edge from V1 to V2
    ct.add_edge(G, V1, V2, n_regs=1)

    self.assertEqual(len(G.nodes()), 2)
    self.assertEqual(len(G.edges()), 1)
    self.assertEqual(len(G['V1']['V2']), 1)
    # access the weight
    self.assertEqual(list(G['V1']['V2'].values())[0]['weight'], 1)

    with self.assertRaises(ValueError):
      ct.add_edge(G, 'p', 'q')

  def test_get_path_weight(self):
    G = ct.create_graph()
    V1 = ct.add_vertex(G, 1)
    V2 = ct.add_vertex(G, 2)
    V3 = ct.add_vertex(G, 5)
    V4 = ct.add_vertex(G, 8)

    ct.add_edge(G, V1, V2, n_regs=3)
    ct.add_edge(G, V2, V3, n_regs=2)
    ct.add_edge(G, V3, V4, n_regs=1)

    self.assertEqual(ct.get_path_weight(G, [V1, V2, V3, V4]), 6)

  def test_get_path_delay(self):
    G = ct.create_graph()
    V1 = ct.add_vertex(G, 1)
    V2 = ct.add_vertex(G, 2)
    V3 = ct.add_vertex(G, 5)
    V4 = ct.add_vertex(G, 8)

    ct.add_edge(G, V1, V2, n_regs=3)
    ct.add_edge(G, V2, V3, n_regs=2)
    ct.add_edge(G, V3, V4, n_regs=1)

    self.assertEqual(ct.get_path_delay(G, [V1, V2, V3, V4]), 16)

  def test_validate_graph(self):
    G = ct.create_graph()
    V1 = ct.add_vertex(G, 1)
    V2 = ct.add_vertex(G, 2)
    V3 = ct.add_vertex(G, 5)
    V4 = ct.add_vertex(G, 8)

    ct.add_edge(G, V1, V2, n_regs=3)
    ct.add_edge(G, V2, V3, n_regs=2)
    ct.add_edge(G, V3, V4, n_regs=1)
    ct.add_edge(G, V3, V1, n_regs=0)
    ct.add_edge(G, V4, V1, n_regs=0)

    ct.validate_graph(G)

    # negate node weight
    G.nodes[V1]['weight'] = -1
    with self.assertRaises(ValueError):
      ct.validate_graph(G)
    G.nodes[V1]['weight'] = 0

    # negate the edge weight
    G[V1][V2][0]['weight'] = -1
    with self.assertRaises(ValueError):
      ct.validate_graph(G)

    G[V1][V2][0]['weight'] = 1
    ct.add_edge(G, V1, V1, n_regs=0)  # zero register self-cycle
    with self.assertRaises(ValueError):
      ct.validate_graph(G)

  def test_compute_clock_period(self):
    """ """
    G = ct.create_graph()
    V1 = ct.add_vertex(G, 1)
    V2 = ct.add_vertex(G, 2)
    V3 = ct.add_vertex(G, 3)
    V4 = ct.add_vertex(G, 4)

    ct.add_edge(G, V1, V2, n_regs=0)
    ct.add_edge(G, V2, V3, n_regs=2)
    ct.add_edge(G, V2, V4, n_regs=0)
    ct.add_edge(G, V1, V4, n_regs=0)

    cp = ct.compute_clock_period(G)
    self.assertEqual(cp, 7)

    G.nodes[V3]['weight'] = 9
    cp = ct.compute_clock_period(G)
    self.assertEqual(cp, 9)


if __name__ == '__main__':
  unittest.main()