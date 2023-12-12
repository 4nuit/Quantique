from qiskit import *

qc = QuantumCircuit(8)
qc.ccx(0,1,4)
qc.ccx(2,4,5)
qc.ccx(3,5,6)
qc.cx(6,7)
qc.ccx(3,5,6)
qc.ccx(2,4,5)
qc.ccx(0,1,4)
qc.measure_all()
qc.draw()
print(qc)