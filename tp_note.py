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

def draw_graph(G, solution, pos):
    default_axes = plt.axes(frameon=True)
    selected_edges = get_selected_edges(solution)
    nx.draw_networkx_edges(G, pos, edgelist=selected_edges, edge_color="r", width=2)
    nx.draw_networkx_nodes(G, pos, node_color="grey", node_size=600, alpha=0.8, ax=default_axes)
    node_labels = {node: str(node) for node in G.nodes()}
    nx.draw_networkx_labels(G, pos=pos, labels=node_labels)

def get_selected_edges(solution):
    selected_edges = E
    return [edge for i, edge in enumerate(selected_edges) if solution[i] == 1]

V = [1, 2, 3, 4, 5, 6, 7]
E = [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6,7)]

G = nx.Graph()
G.add_nodes_from(V)
G.add_edges_from(E)

colors = ["r" for node in G.nodes()]
pos = nx.spring_layout(G)
draw_graph(G, colors, pos)

# Définition du problème Max-Cut comme problème d'optimisation quadratique
qubo = QuadraticProgram()

linear = {}
quadratic = {}
qubo.binary_var('x_12')
qubo.binary_var('x_13')
qubo.binary_var('x_23')
qubo.binary_var('x_45')
qubo.binary_var('x_56')
qubo.binary_var('x_67')

# Définition de la fonction objectif
qubo.minimize(linear={'x_12': -3, 'x_13': -3, 'x_23': -3, 'x_45': -3, 'x_56': -3, 'x_67': -3},
              quadratic={('x_12', 'x_13'): 2, ('x_12', 'x_23'): 2, ('x_13', 'x_23'): 2,('x_45', 'x_56'): 2, ('x_56', 'x_67'): 2},
              constant=0)

# Ajout de la contrainte de somme minimale
qubo.linear_constraint(linear={'x_12': 1, 'x_13': 1, 'x_23': 1, 'x_45': 1, 'x_56': 1, 'x_67': 1},
                       sense='>=', rhs=1, name='c0')

print(qubo.prettyprint())

optimizer = COBYLA()
available_backends = Aer.backends()
sampler = Sampler()
qaoa_mes = QAOA(sampler,optimizer)
qaoa = MinimumEigenOptimizer(qaoa_mes)
result = qaoa.solve(qubo);print(result)

solution = result.x
draw_graph(G, solution, pos)
plt.show()