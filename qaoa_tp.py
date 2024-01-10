import networkx as nx
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute
from qiskit.circuit import Parameter
from qiskit_optimization import QuadraticProgram
from qiskit.utils import QuantumInstance
from qiskit.algorithms.minimum_eigensolvers import QAOA
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler

def draw_graph(G, colors, pos):
    default_axes = plt.axes(frameon=True)
    nx.draw_networkx(G, node_color=colors, node_size=600, alpha=0.8, ax=default_axes, pos=pos)
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)

V = [1, 2, 3, 4, 5]
E = [(1, 2), (1, 3), (2, 3), (3, 4), (4, 5)]

G = nx.Graph()
G.add_nodes_from(V)
G.add_edges_from(E)

colors = ["r" for node in G.nodes()]
pos = nx.spring_layout(G)
draw_graph(G, colors, pos)

# Définition du problème Max-Cut comme problème d'optimisation quadratique
qubo = QuadraticProgram()
for node in G.nodes:
    qubo.binary_var(f'x_{node}')


linear = {}
quadratic = {}
for i, j in G.edges:
    weight = G[i][j].get('weight', 1)
    linear[f'x_{i}'] = linear.get(f'x_{i}', 0) + weight
    linear[f'x_{j}'] = linear.get(f'x_{j}', 0) + weight
    quadratic[f'x_{i}', f'x_{j}'] = -2 * weight

qubo.maximize(constant=0, linear=linear, quadratic=quadratic)
print(qubo.prettyprint())

optimizer = COBYLA()
available_backends = Aer.backends()
sampler = Sampler()
qaoa_mes = QAOA(sampler,optimizer)
qaoa = MinimumEigenOptimizer(qaoa_mes)


result = qaoa.solve(qubo)
print(result)

solution = result.x
colors = ["r" if sol == 0 else "b" for sol in solution]
draw_graph(G, colors, pos)

plt.show()