from PlanarRobot import PlanarRobot
import numpy as np
import matplotlib.pyplot as plt


# ---------- Funções de plotagem dos frames e orientações ----------

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
    plt.plot(*link1, 'ko', markersize=3.5)
    plt.plot(*atuador, 'ko', markersize=3.5)

    plot_orientacao(T0)  # base
    plot_orientacao(T2)  # após elo 1
    plot_orientacao(T4)  # atuador

    margem = 0.5

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


def derivative(data, t):
    data_dot = np.zeros((len(t) - 1, data.shape[1]))
    dt = t[1] - t[0]
    for i in range(1, len(t)):
        data_dot[i - 1] = (data[i] - data[i - 1]) / dt
    return data_dot


def calculate_pos_vel_acc(times, theta1, theta2, robo, t_vector):

    l1 = robo.l1
    l2 = robo.l2
    positions = []
    for time in times:
        idx = np.where(t_vector == time)[0][0]
        th1 = theta1[idx]
        th2 = theta2[idx]
        T0, T1, T2, T3, T4 = robo.get_numeric_frames(th1, th2, l1, l2)
        atuador = T4[0:2, 3]  # x e y
        positions.append(atuador)
    positions = np.array(positions)

    velocities = derivative(positions, times)
    accelerations = derivative(velocities, times[1:])
    return positions, velocities, accelerations


def plot_positions(times, positions):
    fig, axs = plt.subplots(2, 1, figsize=(8,5), sharex=True)

    axs[0].plot(times, positions[:, 0], 'r-')
    axs[0].set_title('Posição X do Punho')
    axs[0].set_ylabel('Posição X (m)')
    axs[0].grid(True)

    axs[1].plot(times, positions[:, 1], 'b-')
    axs[1].set_title('Posição Y do Punho')
    axs[1].set_xlabel('Tempo (s)')
    axs[1].set_ylabel('Posição Y (m)')
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()


def plot_velocities(times, velocities):
    fig, axs = plt.subplots(2, 1, figsize=(8,5), sharex=True)

    axs[0].plot(times[:-1], velocities[:, 0], 'r-')
    axs[0].set_title('Velocidade X do Punho')
    axs[0].set_ylabel('Velocidade X (m/s)')
    axs[0].grid(True)

    axs[1].plot(times[:-1], velocities[:, 1], 'b-')
    axs[1].set_title('Velocidade Y do Punho')
    axs[1].set_xlabel('Tempo (s)')
    axs[1].set_ylabel('Velocidade Y (m/s)')
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()


def plot_accelerations(times, accelerations):
    fig, axs = plt.subplots(2, 1, figsize=(8, 5), sharex=True)

    axs[0].plot(times[:-2], accelerations[:, 0], 'r-')
    axs[0].set_title('Aceleração X do Punho')
    axs[0].set_ylabel('Aceleração X (m/s²)')
    axs[0].grid(True)

    axs[1].plot(times[:-2], accelerations[:, 1], 'b-')
    axs[1].set_title('Aceleração Y do Punho')
    axs[1].set_xlabel('Tempo (s)')
    axs[1].set_ylabel('Aceleração Y (m/s²)')
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()


def plot_xy(data, label):
    data_x, data_y = data[:, 0], data[:, 1]

    plt.figure(figsize=(10, 6))
    plt.plot(data_x, data_y, label=f"{label} do Punho (X vs Y)")
    plt.title(f'{label} do Punho (X vs Y) ao longo do tempo')
    plt.xlabel(f'{label} X (m/s)')
    plt.ylabel(f'{label} Y (m/s)')
    plt.grid(True)
    plt.legend()
    plt.show()


# ---------- Main ----------

if __name__ == '__main__':

    robo_planar = PlanarRobot()

    l1 = l2 = 1
    robo_planar.l1 = l1
    robo_planar.l2 = l2

    t = np.arange(0, 181, 1)
    theta1 = np.arange(-90, 91, 1)
    theta2 = np.arange(-90, 91, 1)
    theta1_rad = np.deg2rad(theta1)
    theta2_rad = np.deg2rad(theta2)

    positions, velocities, accelerations = calculate_pos_vel_acc(t, theta1_rad, theta2_rad, robo_planar, t)

    # Plota posicao, velocidade e aceleração em função do tempo
    plot_positions(t, positions)
    plot_velocities(t, velocities)
    plot_accelerations(t, accelerations)

    # Plota as trajetórias 2D XY para posição, velocidade e aceleração
    plot_xy(positions, 'Posição')
    plot_xy(velocities, 'Velocidade')
    plot_xy(accelerations, 'Aceleração')
