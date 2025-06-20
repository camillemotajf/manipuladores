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
    # | 1  | 0       | th1*      | L1  | 0     |
    # | 2  | 0       | 90 + th2* | 0   | 90    |
    # | 3  | L2 + d3*| 0         | 0   | 0     |
    # |========================================|
    
th1, th2, l1, l2, d3 = sp.symbols('th1 th2 l1 l2 d3', real=True)


T0 = np.eye(4)
A1 = dh_matrix(d=0, th=th1, a=l1, alpha=0, numeric=True)
T1 = T0 @ A1

A2 = dh_matrix(d=0, th=th2, a=l2, alpha=np.deg2rad(90), numeric=True)
T2 = T1 @ A2

A3 = dh_matrix(d=0, th=0, a=d3, alpha=0, numeric=True)
T3 = T2 @ A3

sp.pprint(T3)

L1, L2= 1, 1 # links fixos
D3 = 2 # link variável
TH1, TH2 = np.deg2rad(45), np.deg2rad(-30)

f0 = np.eye(4)
f1 = f0 @ dh_matrix(0, TH1, L1, 0)
f2 = f1 @ dh_matrix(0, np.deg2rad(90)+TH2, 0, np.deg2rad(90))
f3 = f2 @ dh_matrix(L2+D3, 0, 0, 0)

frames = [f0, f1, f2, f3]

plt.figure(1)
fig = plt.axes(projection='3d')

plot_robot(fig, frames, show=True, origin=True)