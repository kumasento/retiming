""" Unit tests for transform.py """

import unittest

import networkx as nx

import retiming.circuit as circuit
import retiming.transform as transform


class TransformTest(unittest.TestCase):
  """ """

  def test_retiming_transform(self):
    """ """
    G = circuit.create_graph()
    vtxs = [circuit.add_vertex(G, i) for i in range(3)]
    nx.add_path(G, vtxs, weight=3)  # add a path
    nx.add_path(G, vtxs, weight=4)  # add another path

    # define the transformation
    r = {vtxs[0]: 1, vtxs[1]: 2}
    Gr = transform.retiming_transform(G, r)

    self.assertEqual(Gr[vtxs[0]][vtxs[1]][0]['weight'],
                     G[vtxs[0]][vtxs[1]][0]['weight'] - r[vtxs[0]] + r[vtxs[1]])

    r[vtxs[0]] = 10
    with self.assertRaises(ValueError):
      transform.retiming_transform(G, r)


if __name__ == '__main__':
  unittest.main()