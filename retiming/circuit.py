""" Graph-based model of the synchronous circuit. """

import networkx as nx

REG_PREFIX = 'R'
VTX_PREFIX = 'V'


def create_graph():
  """ The graph of a circuitry is a multi-edge directed graph. """
  return nx.MultiDiGraph()


def get_vertexes(G):
  """ Get all vertexes in G. """
  assert isinstance(G, nx.MultiDiGraph)

  return [n for n in G.nodes() if n.startswith(VTX_PREFIX)]


def add_vertex(G, delay):
  """ Vertex is the functional element mentioned in the paper.
    Each of them has a propagation delay.

    Args:
      G(nx.MultiDiGraph):
      delay(int): propagation delay
    Returns:
      The label of the vertex
  """
  assert isinstance(G, nx.MultiDiGraph)
  assert isinstance(delay, int)
  assert delay >= 0

  vtxs = get_vertexes(G)
  label = '{}{}'.format(VTX_PREFIX, len(vtxs) + 1)
  G.add_node(label, weight=delay)

  return label


def is_in_graph(G, v):
  """ Check whether a node is in the graph. """
  assert isinstance(v, str)  # v should be a label

  return v in G.nodes()


def add_edge(G, u, v, n_regs=0):
  """ Add an edge from u to v.
  
    u and v should already be in the graph.

    Args:
      G(nx.MultiDiGraph)
      u(str): source
      v(str): destination
      n_regs(int): number of registers on the edge
    Returns:
      None
  """
  assert isinstance(G, nx.MultiDiGraph)
  assert isinstance(u, str)
  assert isinstance(v, str)
  assert isinstance(n_regs, int) and n_regs >= 0

  if not is_in_graph(G, u):
    raise ValueError('u {} is not a node in G.'.format(u))
  if not is_in_graph(G, v):
    raise ValueError('v {} is not a node in G.'.format(v))

  G.add_edge(u, v, weight=n_regs)


def get_path_weight(G, path):
  """ Get the total weight of all vertexes and edges connecting them. 
  
  Args:
    G(nx.MultiDiGraph)
    path(list): a list of node labels
  Returns:
    A sum of all weight
  """
  assert isinstance(G, nx.MultiDiGraph)

  # convert to an edge path
  edges = list(nx.utils.pairwise(path))

  sum_of_weight = 0
  for i, (u, v) in enumerate(edges):
    # edge weights (multiple edges)
    for d in G[u][v].values():
      sum_of_weight += d['weight']

  return sum_of_weight


def get_path_delay(G, path):
  """ Get the total amount of delay of vertexes on the path. """
  assert isinstance(G, nx.MultiDiGraph)

  return sum([G.nodes[n]['weight'] for n in path])


def validate_graph(G):
  """ Validate whether the graph satisfies conditions mentioned 
    in the paper. """
  assert isinstance(G, nx.MultiDiGraph)

  # check nodes
  for v, w in G.nodes.data('weight'):
    if w < 0:
      raise ValueError('Node "{}" has negative delay {}.'.format(v, w))

  # check edges
  for u, v, w in G.edges.data('weight'):
    if w < 0:
      raise ValueError(
          'Number of registers between nodes "{}" and "{}" is negative: {}.'.
          format(u, v, w))

  # check cycles
  for path in nx.simple_cycles(G):
    if get_path_weight(G, path) == 0:
      raise ValueError(
          'There should be at least an edge in the cycle "{}" that has positive weight.'
          .format(path))


def compute_clock_period(G):
  """ Implements Algorithm-CP in the paper. """

  # create a subgraph with zero-weight edges
  # TODO: re-factorise as a function
  edges = [e for e in G.edges.data('weight') if e[2] == 0]
  G0 = create_graph()  # the subgraph
  G0.add_nodes_from(G.nodes(data=True))
  G0.add_weighted_edges_from(edges)

  # topological sort
  vtxs = nx.topological_sort(G0)  # G0 doesn't contain cycles

  # initialise the delta LUT
  delta = {}
  for v in vtxs:
    in_edges = G0.in_edges(v)
    if not in_edges:
      delta[v] = G0.nodes[v]['weight']  # init
    else:
      delta[v] = 0  # min
      for u, _ in in_edges:
        delta[v] = max(delta[v], delta[u] + G0.nodes[v]['weight'])

  # return the maximal value of all delta values
  return max(delta.values())