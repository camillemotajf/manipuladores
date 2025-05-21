import sympy as sym

class PlanarRobot:
    def __init__(self):
        self.theta1, self.theta2 = sym.symbols('th1, th2')
        self.l1, self.l2 = sym.symbols('l1 l2')


    def Rz(self, theta):
        """
            Matriz de Rotação em torno de z (YAW) do Robo Planar
        """

        R = sym.Matrix([
            [sym.cos(theta), -sym.sin(theta), 0, 0],
            [sym.sin(theta), sym.cos(theta), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        return R
    
    def Tz(self, dx, dy, dz): 
        """ 
        Matriz de Translação para o Robo
        """

        T = sym.Matrix([
            [1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]
        ])
        return T
    
    def forward_kinematics(self):
        """
        Modelo cinemático para um Robo Planar de juntas l1 e l2
        
        """
        T1 = self.Rz(self.theta1) @ self.Tz(self.l1, 0, 0)
        T2 = self.Rz(self.theta2) @ self.Tz(self.l2, 0, 0)
        T_total = T1 @ T2
        return T1, T_total
    
    def set_joint_angles(self, theta1, theta2):
        # Atualiza os ângulos das juntas
        self.theta1_val = theta1
        self.theta2_val = theta2


if __name__ == '__main__':
    robo = PlanarRobot()
    print("Theta1:", robo.theta1)
    print("Theta2:", robo.theta2)
    
    T = robo.forward_kinematics()
    print("Forward Kinematics Transformation Matrix:")
    sym.pprint(T)  

