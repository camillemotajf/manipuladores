import sympy as sp
import numpy as np

def dh_matrix( d,th,a,alpha,numeric=False):

    if numeric:
        d, th, a, alpha = sp.symbols('d th a alpha', real=True)

        Tx = sp.Matrix([[1, 0, 0, a],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])

        Tz = sp.Matrix([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, d],
                        [0, 0, 0, 1]])

        Rx = sp.Matrix([[1,     0        ,      0        ,0],
                        [0, sp.cos(alpha), -sp.sin(alpha),0],
                        [0, sp.sin(alpha),  sp.cos(alpha),0],
                        [0,     0        ,      0        ,1]])

        Rz = sp.Matrix([[sp.cos(th), -sp.sin(th), 0, 0],
                        [sp.sin(th),  sp.cos(th), 0, 0],
                        [    0        ,      0        , 1, 0],
                        [    0        ,      0        , 0, 1]])
        
        return sp.simplify(Tz @ Rz @ Tx @ Rz )
    
    else:
        Tx = np.array([[1, 0, 0, a],
                    [0,1,0,0],
                    [0,0,1,0],
                    [0,0,0,1]])
        Rx = np.array([[1,     0        ,      0        ,0],
                    [0, np.cos(alpha), -np.sin(alpha),0],
                    [0, np.sin(alpha),  np.cos(alpha),0],
                    [0,     0        ,      0        ,1]])
        Tz = np.array([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, d],
                    [0, 0, 0, 1]])
        Rz = np.array([[np.cos(th), -np.sin(th), 0, 0],
                    [np.sin(th),  np.cos(th), 0, 0],
                    [    0        ,      0        , 1, 0],
                    [    0        ,      0        , 0, 1]])
            
        return Tz @ Rz @ Tx @ Rx



