from PlanarRobot import PlanarRobot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

robo_planar = PlanarRobot()

# Setar o comprimento do robo (unitario)
l1 = l2 = 1

# vetor tempo
t = np.arange(0, 181, 1)  # de 0s até 180s

# ângulos das juntas
theta1 = np.arange(-90, 91, 1) 
theta2 = np.arange(-90, 91, 1)  

theta1_rad = np.deg2rad(theta1)
theta2_rad = np.deg2rad(theta2)

# posição com variaveis simbolicas
T1_sym, T_total_sym = robo_planar.forward_kinematics()
T1_sym = T1_sym.subs({robo_planar.l1: l1, robo_planar.l2: l2})
T_total_sym = T_total_sym.subs({robo_planar.l1: l1, robo_planar.l2: l2})

pos = []

for th1, th2 in zip(theta1_rad, theta2_rad):
    T1_num = T1_sym.subs({robo_planar.theta1: th1, robo_planar.theta2: th2})
    T_total_num = T_total_sym.subs({robo_planar.theta1: th1, robo_planar.theta2: th2})
    pos.append((T1_num, T_total_num))
    

dados = []

for tempo, (T1_num, T_total_num) in enumerate(pos):
    # Base
    x_base, y_base = 0, 0

    # Junta 1 (fim do primeiro link)
    x_junta1 = float(T1_num[0, 3])
    y_junta1 = float(T1_num[1, 3])

    # Efetuador (fim do segundo link)
    x_efet = float(T_total_num[0, 3])
    y_efet = float(T_total_num[1, 3])

    dados.append({
            'tempo (s)': tempo,
            'x_base': x_base, 'y_base': y_base,
            'x_junta1': x_junta1, 'y_junta1': y_junta1,
            'x_efetuador': x_efet, 'y_efetuador': y_efet
        })
    
df = pd.DataFrame(dados)

plt.figure(figsize=(8, 8))

plt.plot(df['x_junta1'], df['y_junta1'], 'b--', label='Trajetória Junta 1')
plt.plot(df['x_efetuador'], df['y_efetuador'], 'r--', label='Trajetória Efetuador')

amostras = np.linspace(0, len(df) - 1, 10, dtype=int)  # escolher 10 poses

for idx in amostras:
    x = [df.loc[idx, 'x_base'], df.loc[idx, 'x_junta1'], df.loc[idx, 'x_efetuador']]
    y = [df.loc[idx, 'y_base'], df.loc[idx, 'y_junta1'], df.loc[idx, 'y_efetuador']]
    
    plt.plot(x, y, 'ko-', linewidth=2)  
    plt.plot(x[0], y[0], 'go', markersize=8)  
    plt.plot(x[1], y[1], 'bo', markersize=8)  
    plt.plot(x[2], y[2], 'ro', markersize=8)  

plt.title('Trajetória e Estrutura do Robô Planar')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.grid(True)
plt.axis('equal')
plt.legend()
plt.show()
