import sympy as sym
import numpy as np
import matplotlib.pyplot as plt


class PlanarRobot:
    def __init__(self):
        self.theta1, self.theta2 = sym.symbols('th1 th2')
        self.l1, self.l2 = sym.symbols('l1 l2')

    def Rz(self, theta):
        """Matriz de rotação em torno do eixo Z"""
        return sym.Matrix([
            [sym.cos(theta), -sym.sin(theta), 0, 0],
            [sym.sin(theta),  sym.cos(theta), 0, 0],
            [0,               0,              1, 0],
            [0,               0,              0, 1]
        ])

    def Tz(self, dx, dy, dz):
        """Matriz de translação"""
        return sym.Matrix([
            [1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]
        ])

    def forward_kinematics(self):
        """Cinemática direta"""
        T0 = sym.eye(4)  # Frame base

        T1 = T0 @ self.Rz(self.theta1)                  # Rotação da junta 1
        T2 = T1 @ self.Tz(self.l1, 0, 0)                # Translação do link 1
        T3 = T2 @ self.Rz(self.theta2)                  # Rotação da junta 2
        T4 = T3 @ self.Tz(self.l2, 0, 0)                # Translação do link 2 (efetuador)

        return T0, T1, T2, T3, T4

    def get_numeric_frames(self, theta1_val, theta2_val, l1_val, l2_val):
        """Gera as matrizes numéricas dado os ângulos e comprimentos"""
        T0, T1, T2, T3, T4 = self.forward_kinematics()

        subs = {
            self.theta1: theta1_val,
            self.theta2: theta2_val,
            self.l1: l1_val,
            self.l2: l2_val
        }

        T0 = np.array(T0.subs(subs)).astype(np.float64)
        T1 = np.array(T1.subs(subs)).astype(np.float64)
        T2 = np.array(T2.subs(subs)).astype(np.float64)
        T3 = np.array(T3.subs(subs)).astype(np.float64)
        T4 = np.array(T4.subs(subs)).astype(np.float64)

        return T0, T1, T2, T3, T4


if __name__ == '__main__':
    robo = PlanarRobot()

    # Parâmetros
    l1 = 1
    l2 = 1
    theta1 = -np.pi / 2
    theta2 = np.pi / 2

    # Frames
    frames = robo.get_numeric_frames(theta1, theta2, l1, l2)
    frames_symbolic = robo.forward_kinematics()
    atuador_symbolic = sym.simplify(frames_symbolic[4])

    print("\n==========================================================")
    print("     Questão 2 - Letra (a): ")
    print("==========================================================")
    print("Frame final do Atuador do Braço - Modelo Simbolico\n")
    sym.pprint(atuador_symbolic)