import numpy as np

def Rz(theta):
    """Matriz de rotação em torno do eixo Z"""
    return np.array([
        [np.cos(theta), -np.sin(theta), 0, 0],
        [np.sin(theta),  np.cos(theta), 0, 0],
        [0,               0,              1, 0],
        [0,               0,              0, 1]
    ])

def Tz(dx, dy, dz):
        """Matriz de translação"""
        return np.array([
            [1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]
        ])

def robo_planar(l, th1, th2, th3):
    # Frame Inercial
    T0 = np.eye(4)
    final_frame = T0 @ Rz(th1) @ Tz(l,0,0) @ Rz(th2) @ Tz(l,0,0) @ Rz(th3)@ Tz(l,0,0)
    final_pos = final_frame[:2,3]
    phi = np.rad2deg(np.arctan2(final_frame[1,0], final_frame[0,0]))
    return final_pos, phi

def cal_angles(passos, diretion):
    angulo_passo = 1.8
    theta = np.deg2rad(passos*angulo_passo*diretion)
    return theta

if __name__ == "__main__":
     link = 0.3
     th1 = cal_angles(50, 1)
     th2 = cal_angles(50, -1)
     th3 = cal_angles(50, 1)
     pos, phi = robo_planar(link, th1=th1, th2=th2, th3=th3)
     print(pos)
     print(phi)


    

