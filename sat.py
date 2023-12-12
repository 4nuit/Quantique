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

def ampli(n):
    am = QuantumCircuit(n)
    for i in range(n):
        am.h(i)
        am.x(i)
    
    am.h(n-1)
    am.mcx([i for i in range(n-1)],i) ## multi controlled not (toffoli(n))
    am.h(n-1)

    for i in range(n):
        am.x(i)
        am.h(i)
    return am

amp = ampli(10)
amp.measure_all()
amp.draw()
print(amp)

"""
grover = QuantumCircuit(3)
grover.h(0)
grover.h(1)
grover.x(2)
grover.h(2)

grover = grover.compose(oracle).compose(ampli)
print(grover)
"""