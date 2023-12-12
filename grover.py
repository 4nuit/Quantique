from qiskit import *

oracle = QuantumCircuit(3)
oracle.x(0)
oracle.ccx(0,1,2)
oracle.x(0)
oracle.measure_all()
oracle.draw()
print(oracle)

backend = Aer.get_backend('qasm_simulator')
job = execute(oracle,backend)
my_results = job.result()
print(my_results.get_counts(oracle))

ampli = QuantumCircuit(2)
ampli.h(0)
ampli.h(1)
ampli.x(0)
ampli.x(1)
ampli.cz(0,1)
ampli.x(0)
ampli.x(1)
ampli.h(0)
ampli.h(1)

ampli.draw()
print(ampli)

grover = QuantumCircuit(3)
grover.h(0)
grover.h(1)
grover.x(2)
grover.h(2)

grover = grover.compose(oracle).compose(ampli)
print(grover)