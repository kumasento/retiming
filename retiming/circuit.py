""" Graph-based model of the synchronous circuit. """

import networkx as nx

REG_PREFIX = 'R'
VTX_PREFIX = 'V'


def create_graph():
  """ The graph of a circuitry is a multi-edge directed graph. """
  return nx.MultiDiGraph()


def get_registers(G):
  """ Get all registers in G.
  
    Registers are labelled with an 'R' prefix.
  """
  assert isinstance(G, nx.MultiDiGraph)

  return [n for n in G.nodes() if n.startswith(REG_PREFIX)]


def get_vertexes(G):
  """ Get all vertexes in G. """
  assert isinstance(G, nx.MultiDiGraph)

  return [n for n in G.nodes() if n.startswith(VTX_PREFIX)]


def add_register(G):
  """ Add a register to a graph.
  
    Returns:
      A str typed label.
  """
  assert isinstance(G, nx.MultiDiGraph)

  regs = get_registers(G)
  label = '{}{}'.format(REG_PREFIX, len(regs) + 1)

  # simply add a new node
  G.add_node(label)

  return label


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
  G.add_node(label, delay=delay)

  return label


def is_in_graph(G, v):
  """ Check whether a node is in the graph. """


def add_edge(G, u, v):
  """ Add an edge from u to v.
  
    u and v should already be in the graph.
  """
  assert isinstance(G, nx.MultiDiGraph)
  assert isinstance(u, str)
  assert isinstance(v, str)

  if not u.startswith(REG_PREFIX) and not u.startswith(VTX_PREFIX):
    raise ValueError('u should be a register or a vertex')
  if not v.startswith(REG_PREFIX) and not v.startswith(VTX_PREFIX):
    raise ValueError('v should be a register or a vertex')

  G.add_edge(u, v)