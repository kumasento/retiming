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
  assert isinstance(v, str)  # v should be a label

  if v.startswith(REG_PREFIX):
    # TODO: cache this information in the graph
    regs = get_registers(G)
    return v in regs

  if v.startswith(VTX_PREFIX):
    # TODO: cache this information in the graph
    vtxs = get_vertexes(G)
    return v in vtxs

  raise ValueError(
      'v is not prefixed properly for a node in the circuit graph.')


def add_edge(G, u, v):
  """ Add an edge from u to v.
  
    u and v should already be in the graph.
  """
  assert isinstance(G, nx.MultiDiGraph)
  assert isinstance(u, str)
  assert isinstance(v, str)

  if not is_in_graph(G, u):
    raise ValueError('u {} is not a node in G.'.format(u))
  if not is_in_graph(G, v):
    raise ValueError('v {} is not a node in G.'.format(v))

  G.add_edge(u, v)