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

def plot_robot_frames(time, theta1, theta2, robo): 

    l1 = robo.l1 
    l2 = robo.l2

    idx = np.where(t == time)[0][0]

    th1 = theta1[idx]
    th2 = theta2[idx]

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

def plot_trajectory_over_time(times, theta1, theta2, robo, t_vector, salto=20):
    l1 = robo.l1
    l2 = robo.l2
    
    # Lista para armazenar as posições (x,y) do atuador nos tempos selecionados
    x_pos = []
    y_pos = []

    # Seleciona os tempos pulando de salto em salto
    tempos_selecionados = times[::salto]

    for time in tempos_selecionados:
        idx = np.where(t_vector == time)[0][0]
        th1 = theta1[idx]
        th2 = theta2[idx]
        
        T0, T1, T2, T3, T4 = robo.get_numeric_frames(th1, th2, l1, l2)
        
        atuador = T4[0:2, 3]
        x_pos.append(atuador[0])
        y_pos.append(atuador[1])
    
    # Plot único com as posições ao longo do tempo
    plt.figure(figsize=(7,7))
    plt.plot(x_pos, y_pos, 'o-', label='Trajetória atuador')
    
    # Marcar cada ponto com o tempo correspondente
    for (x, y, time) in zip(x_pos, y_pos, tempos_selecionados):
        plt.text(x + 0.03, y + 0.03, f'{time}s', fontsize=8)
    
    plt.title('Trajetória XY do atuador ao longo do tempo')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.axis('equal')
    plt.legend()
    plt.show()

def plot_robot_trajectory_with_links(times, theta1, theta2, robo, t_vector, salto=20):
    l1 = robo.l1
    l2 = robo.l2
    label = False

    plt.figure(figsize=(7, 7))
    
    # Para cada tempo espaçado
    for time in times[::salto]:

        idx = np.where(t_vector == time)[0][0]
        th1 = theta1[idx]
        th2 = theta2[idx]

        T0, T1, T2, T3, T4 = robo.get_numeric_frames(th1, th2, l1, l2)
        
        origem = T0[0:2, 3]
        link1 = T2[0:2, 3]
        atuador = T4[0:2, 3]
        
        # Plota os links como linhas
        plt.plot([origem[0], link1[0]], [origem[1], link1[1]], 'b-', linewidth=1)
        plt.plot([link1[0], atuador[0]], [link1[1], atuador[1]], 'b-', linewidth=1)
        plt.xticks(np.arange(-3, 3.5, 0.5))
        plt.yticks(np.arange(-3, 3.5, 0.5))
        
        if not label:
            plt.plot(*origem, 'ko', label='Origem', markersize=4)
            plt.plot(*atuador, 'go', label='Atuador', markersize=4)
            label = True
        else:
            plt.plot(*origem, 'ko', markersize=4)
            plt.plot(*atuador, 'go', markersize=4)

        plt.plot(*link1, 'ro', markersize=4)  # sem label

        
        # Adiciona texto com o tempo próximo ao atuador
        plt.text(atuador[0] + 0.03, atuador[1] + 0.03, f'{time}s', fontsize=8)
    
    plt.title('Trajetória do robô com links em diferentes tempos')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.axis('equal')
    
    margem = l1 + l2 + 0.5
    plt.xlim(-margem, margem)
    plt.ylim(-margem, margem)
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
    plot_robot_frames(time=0, theta1=theta1_rad, theta2=theta1_rad, robo=robo_planar)

    # Plotando em t = 30s
    plot_robot_frames(time=30, theta1=theta1_rad, theta2=theta1_rad, robo=robo_planar)

    # Plotando t = 60s
    plot_robot_frames(time=60, theta1=theta1_rad, theta2=theta1_rad, robo=robo_planar)

    plot_trajectory_over_time(t, theta1_rad, theta2_rad, robo_planar, t, salto=20)

    plot_robot_trajectory_with_links(t, theta1_rad, theta2_rad, robo_planar, t, salto=20)
    

