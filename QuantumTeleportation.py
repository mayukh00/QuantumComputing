#!/usr/bin/env python
# coding: utf-8

# In[20]:

import numpy as np
# Importing standard Qiskit libraries
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import IBMQ, Aer, transpile, assemble
from qiskit.visualization import plot_histogram, plot_bloch_multivector, array_to_latex
from qiskit.extensions import Initialize
from qiskit.ignis.verification import marginal_counts
from qiskit.quantum_info import random_statevector


# In[5]:


qr= QuantumRegister(3, name="q")  #3qubits
crz= ClassicalRegister(1, name="crz")  #2 claassical bits in two different registers
crx= ClassicalRegister(1, name="crx")
teleportation_circuit= QuantumCircuit(qr, crz, crx)
#teleportation_circuit.draw()


# In[6]:


def create_bell_pair(qc, a, b): #creates a bell pair in qc using qubit a and b
    qc.h(a)
    qc.cx(a,b)


# In[7]:


#step 1
create_bell_pair(teleportation_circuit, 1, 2)
teleportation_circuit.draw()


# In[8]:


#let say Alice owns q1 and Bob ows q2 after they part ways.
def Alice_measurement_state(qc, psi, a):
    qc.cx(psi,a)
    qc.h(psi)


# In[9]:


# step 2
teleportation_circuit.barrier()
Alice_measurement_state(teleportation_circuit, 0, 1)
teleportation_circuit.draw()


# In[10]:


def measure_and_send(qc, a, b):  #measure qubits a,b and "send" to bob
    qc.measure(a,0)
    qc.measure(b,1)


# In[12]:


# step 3

measure_and_send(teleportation_circuit,0,1)
teleportation_circuit.draw()


# In[13]:


def bob_gates(qc, qubit, crz, crx):
    qc.x(qubit).c_if(crx,1)  #we use c_if to control gate with classical bits instead of qubit
    qc.z(qubit).c_if(crz,1)  # apply X,Z gates only if classical registers are in state 1


# In[14]:


# Step 4
teleportation_circuit.barrier()
bob_gates(teleportation_circuit, 2, crz, crx)
teleportation_circuit.draw() #complete Q-Teleportation circuit


# In[16]:


# Create random 1-qubit state
psi = random_statevector(2)

# Display it nicely
display(array_to_latex(psi, prefix="|\\psi\\rangle ="))
# Show it on a Bloch sphere
plot_bloch_multivector(psi)


# In[17]:


init_gate= Initialize(psi)
init_gate.label= "init"


# In[18]:


# Overall teleportation setup 

qr= QuantumRegister(3, name="q")  
crz= ClassicalRegister(1, name="crz")
crx= ClassicalRegister(1, name="crx")
qc= QuantumCircuit(qr, crz, crx)

#Step 0: 1st initialize Alice's q0
qc.append(init_gate, [0])
qc.barrier()

#Step1 create entangled bell state btw alice and bob
create_bell_pair(qc, 1, 2)
qc.barrier()

#Step2 measurement state
Alice_measurement_state(qc, 0, 1)
qc.barrier()

#Step3  alice sends the classical bits to bob
measure_and_send(qc, 0, 1)
qc.barrier()

#Step4 bob decoded qubits
bob_gates(qc, 2, crz, crx)

qc.draw()



# In[19]:


sim= Aer.get_backend('aer_simulator')
qc.save_statevector()
out_vector=sim.run(qc).result().get_statevector()
plot_bloch_multivector(out_vector)
