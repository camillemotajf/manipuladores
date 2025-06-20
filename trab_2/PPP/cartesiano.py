import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dh_matrix import dh_matrix
from plots import plot_robot


    # |========================================|
    # | Ai | d       | theta     | a   | alpha |
    # |----|---------|-----------|-----|-------|
    # | A1 | L0      |  0        | 0   | -90   |
    # | A2 | L1 + d1*| -90       | 0   | -90   |
    # | A3 | L2 + d2*|  90       | 0   | -90   |
    # | A4 | d3*     |  0        | 0   |  0    |
    # |========================================|
    
l0, l1, l2, d1, d2, d3 = sp.symbols('l0, l1, l2, d1, d2, d3', real=True)


T0 = np.eye(4)
A1 = dh_matrix(d=l0, th=0, a=0, alpha=np.deg2rad(-90), numeric=True)
T1 = T0 @ A1

A2 = dh_matrix(d=l1+d1, th=np.deg2rad(-90), a=0, alpha=np.deg2rad(-90), numeric=True)
T2 = T1 @ A2

A3 = dh_matrix(d=l2+d2, th=np.deg2rad(90), a=0, alpha=np.deg2rad(-90), numeric=True)
T3 = T2 @ A3

A4 = dh_matrix(d=d3, th=0, a=0, alpha=0, numeric=True)
T4 = T3 @ A4

sp.pprint(T4)

L0, L1, L2 = 1, 1, 1 # links fixos
# D1, D2, D3 = 0, 0, 0 # links variaveis
D1, D2, D3 = 1, 2, 3 # links variaveis

f0 = np.eye(4)
f1 = f0 @ dh_matrix(d=L0, th=0, a=0, alpha=np.deg2rad(-90))
f2 = f1 @ dh_matrix(d=L1+D1, th=np.deg2rad(-90), a=0, alpha=np.deg2rad(-90))
f3 = f2 @ dh_matrix(d=L2+D2, th=np.deg2rad(90), a=0, alpha=np.deg2rad(-90))
f4 = f3 @ dh_matrix(d=D3, th=0, a=0, alpha=0)

frames = [f0, f1, f2, f3, f4]

plt.figure(1)
fig = plt.axes(projection='3d')

plot_robot(fig, frames, show=True, origin=True)