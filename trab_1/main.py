from PlanarRobot import PlanarRobot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_orientacao(T, cor='k'):
    pos = T[0:2, 3]     # posição (origem do frame)
    x_axis = T[0:2, 0]  # vetor da direção do eixo x
    y_axis = T[0:2, 1]  # vetor da direção do eixo y
    escala = 0.4        # tamanho das setas

    plt.quiver(*pos, *x_axis, color='r', scale=1/escala, scale_units='xy', angles='xy', width=0.005)
    plt.quiver(*pos, *y_axis, color='g', scale=1/escala, scale_units='xy', angles='xy', width=0.005)

def plot_robot_frames(time, robo): 

    l1 = robo.l1 
    l2 = robo.l2

    idx = np.where(t == time)[0][0]

    th1 = theta1_rad[idx]
    th2 = theta2_rad[idx]

    # Plot da posição e eixos no tempo 0s
    T0, T1, T2, T3, T4 = robo.get_numeric_frames(th1, th2, l1, l2)

    origem = T0[0:2, 3]
    link1 = T2[0:2, 3]
    atuador = T4[0:2, 3]

    plt.figure(figsize=(6, 6))

    plt.plot([origem[0], link1[0]], [origem[1], link1[1]], 'b-', linewidth=1, label='Links')
    plt.plot([link1[0], atuador[0]], [link1[1], atuador[1]], 'b-', linewidth=1)

    plt.text(origem[0] + 0.05, origem[1] + 0.08, 'T_{0}', fontsize=8)
    plt.text(link1[0] + 0.05, link1[1] + 0.08, 'T_{1}', fontsize=8)
    plt.text(atuador[0] + 0.05, atuador[1] + 0.08, 'T_{2}', fontsize=8)

    plt.plot(*origem, 'ko', markersize=3.5)
    plt.plot(*link1, 'ko' ,markersize=3.5)
    plt.plot(*atuador, 'ko',markersize=3.5)

    plot_orientacao(T0)  # base
    plot_orientacao(T2)  # após elo 1
    plot_orientacao(T4)  # atuador

    margem = 0.5
    # Visualização final
    plt.title(f'Posição do Robot em t = {time}s')
    plt.axis('equal')
    plt.xticks(np.arange(-3, 3.5, 0.5))
    plt.yticks(np.arange(-3, 3.5, 0.5))
    plt.grid(True)
    plt.xlim(-l1 - l2 - margem, l1 + l2 + margem)
    plt.ylim(-l1 - l2 - margem, l1 + l2 + margem)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()

if __name__ == '__main__':    
    robo_planar = PlanarRobot()

    # Setar o comprimento do robo (unitario)
    l1 = l2 = 1
    robo_planar.l1 = l1
    robo_planar.l2 = l2

    # vetor tempo
    t = np.arange(0, 181, 1)  # de 0s até 180s

    # ângulos das juntas
    theta1 = np.arange(-90, 91, 1) 
    theta2 = np.arange(-90, 91, 1)  

    theta1_rad = np.deg2rad(theta1)
    theta2_rad = np.deg2rad(theta2)

    # Plotando em t = 0s
    plot_robot_frames(0, robo_planar)

    # Plotando em t = 90s
    plot_robot_frames(90, robo_planar)

    # Plotando t = 180 s
    plot_robot_frames(180, robo_planar)
    

