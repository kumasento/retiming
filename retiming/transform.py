""" All the transformations that can be applied on a circuit graph. """

import networkx as nx


def retiming_transform(G, r):
  """ Apply retiming by inserting a lag value to each vertex.
  
  Args:
    G(nx.MultiDiGraph)
    r(dict): mapping for vertexes to retiming labels
  Returns:
    A transformed graph.
  """
  assert isinstance(G, nx.MultiDiGraph)
  assert isinstance(r, dict)

  G_ = G.copy()
  for u, v, i in G.edges(keys=True):
    if u in r:
      G_[u][v][i]['weight'] -= r[u]
    if v in r:
      G_[u][v][i]['weight'] += r[v]

    # validation
    if not isinstance(G_[u][v][i]['weight'], int):
      raise TypeError('Values in retiming {} involve non-integers'.format(r))
    if G_[u][v][i]['weight'] < 0:
      raise ValueError(
          'Retiming "{r}" turns the weight of an edge ({u}, {v}, {i}) into a negative value: {w}.'
          .format(r=r, u=u, v=v, i=i, w=G_[u][v][i]['weight']))

  return G_