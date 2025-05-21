import sympy as sym

class PlanarRobot:
    def __init__(self):
        self.theta = sym.symbols('th')
        self.theta1, self.theta2 = sym.symbols('th1, th2')
        self.dx, self.dy, self.dz = sym.symbols('dx, dy, dz')


        def Rz(theta):

            R = sym.Matrix([
                [sym.cos(theta), -sym.sen(theta), 0, 0],
                [sym.sen(theta), sym.cos(theta), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])
            return R
        
        def Tz(dx, dy, dz): 
            T = sym.Matrix([
                [1, 0, 0, dx],
                [0, 1, 0, dy],
                [0, 0, 1, dz],
                [0, 0, 0, 1]
            ])
            return T
        
        # def Model()
        pass


if __name__ == '__main__':
    robo = PlanarRobot()
    print(robo.theta1, robo.theta2)   

