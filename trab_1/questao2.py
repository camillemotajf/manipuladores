import numpy as np

def calcula_L1_L2(base, effector, theta1_deg, theta2_deg):
    """
    Calcula os comprimentos L1 e L2 do robô planar 2R
    """
    x0, y0 = base
    xe, ye = effector
    theta1 = np.radians(theta1_deg)
    theta2 = np.radians(theta2_deg)
    
    # Vetor posição relativa do efetuador em relação à base
    dx = xe - x0
    dy = ye - y0
    
    A = np.array([
        [np.cos(theta1), np.cos(theta1 + theta2)],
        [np.sin(theta1), np.sin(theta1 + theta2)]
    ])
    b = np.array([dx, dy])
    
    L = np.linalg.solve(A, b)
    
    L1, L2 = L[0], L[1]
    return L1, L2

base = (0, 0)
effector = (13, 26) 
theta1_deg = 30
theta2_deg = 60

L1, L2 = calcula_L1_L2(base, effector, theta1_deg, theta2_deg)
print(f'Comprimento L1 = {L1:.2f} cm')
print(f'Comprimento L2 = {L2:.2f} cm')
