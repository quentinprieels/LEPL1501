import matplotlib.pyplot as plt
from main import *
from variables import to_degrees

mi = maximum_inclination()


# --- Creat graphs ---
def graph_crane_motion():
    """
    :return: Draws a graph that shows the amplitude of the crane's arms over time
    """
    plt.figure(1)
    plt.title("Motion of the crane")
    plt.plot(t, grue2_angle * to_degrees, label="Angle 2d piece")
    plt.plot(t, grue3_angle * to_degrees, label="Angle 3d piece")
    plt.plot(t, grue4_angle * to_degrees, label="Angle 4th piece")
    plt.xlabel("Time [s]")
    plt.ylabel("Angles [°]")
    plt.legend()
    plt.show()


def graph_centers_evolution():
    """
    :return: Draws a graph that shows the position of the center of gravity and thrust over time
    """
    plt.figure(2)
    plt.suptitle("Center of gravity and Center Thrust")
    plt.subplot(2, 1, 1)
    plt.plot(t, cg_list_x, '-r', label="Center of gravity - x")
    plt.xlabel("Time [s]")
    plt.ylabel("Position x [m]")
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.plot(t, cg_list_z, '-r', label="Center of gravity - z")
    plt.xlabel("Time [s]")
    plt.ylabel("Position x [m]")
    plt.legend()
    plt.show()


def graph_theta_omega():
    plt.figure(3)
    plt.suptitle("ω and θ")

    plt.subplot(3, 1, 1)
    plt.plot(t, theta * to_degrees)
    plt.plot([0, t[-1]], [maximum_inclination() * to_degrees, maximum_inclination() * to_degrees], '--r',
             label="Maximum inlinaison")
    plt.plot([0, t[-1]], [-maximum_inclination() * to_degrees, -maximum_inclination() * to_degrees], '--r')
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("θ [°]")

    plt.subplot(3, 1, 2)
    plt.plot(t, omega * to_degrees)
    plt.xlabel("Time [s]")
    plt.ylabel("ω [° / s]")

    plt.subplot(3, 1, 3)
    plt.plot(t, a * to_degrees)
    plt.xlabel("Time [s]")
    plt.ylabel("a [rad / s ** 2]")

    plt.show()


def graph_phase_diagram():
    plt.figure(4)
    plt.title("Phase Diagram")
    plt.plot(theta, omega)
    plt.xlabel("θ [°]")
    plt.ylabel("ω [°]")
    plt.show()


def graph_energy():
    E_G = mass_sum * g * (cg_list_x - cg_list_x[0])
    E_C = -M * g * (y_C - y_C[0])
    E_K = Im * omega * omega / 2
    E_A = -Ca * theta


# --- Lunch program ---
graph_crane_motion()
graph_centers_evolution()
graph_theta_omega()
graph_phase_diagram()
