import matplotlib.pyplot as plt
from compet.main import *
from compet.variables import to_degrees

mi = maximum_inclination()


# --- Creat graphs ---
def graph_crane_motion():
    """
    :return: Draws a graph that shows the amplitude of the crane's arms over time
    """
    plt.figure(1)
    plt.title("Motion of the crane")
    plt.plot(t, grue2_angle * to_degrees, label="Angle 2nd piece")
    plt.plot(t, grue3_angle * to_degrees, label="Angle 3rd piece")
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
    plt.plot(t, cp_list_x, label="Center Thrust - x")
    plt.xlabel("Time [s]")
    plt.ylabel("Position x [m]")
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.plot(t, cg_list_z, '-r', label="Center of gravity - z")
    plt.plot(t, cp_list_z, label="Center Thrust - z")
    plt.xlabel("Time [s]")
    plt.ylabel("Position z [m]")
    plt.legend()
    plt.show()


def graph_theta_omega():
    plt.figure(3)
    plt.suptitle("ω and θ")

    plt.subplot(3, 1, 1)
    plt.plot(t, theta * to_degrees)
    plt.plot([0, t[-1]], [maximum_inclination() * to_degrees, maximum_inclination() * to_degrees], '--r',
             label="Maximum inclination")
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
    plt.plot(theta * to_degrees, omega * to_degrees)
    plt.xlabel("θ [°]")
    plt.ylabel("ω [°/s]")
    plt.show()


def graph_energy():
    """
    :return: Creates the graphics of the energy
    """
    plt.figure(5)
    plt.suptitle("Energy")
    plt.subplot(3, 1, 1)
    plt.plot(t, E_g, label="Gravitational Energy")
    plt.xlabel("Time [s]")
    plt.ylabel("Energy [J]")
    plt.legend()
    plt.subplot(3, 1, 2)
    plt.plot(t, E_p, label="Thrust Energy")
    plt.xlabel("Time [s]")
    plt.ylabel("Energy [J]")
    plt.legend()
    plt.subplot(3, 1, 3)
    plt.plot(t, E_k, label="Kinetics Energy")
    plt.xlabel("Time [s]")
    plt.ylabel("Energy [J]")
    plt.legend()
    plt.show()


# --- Lunch program ---
graph_crane_motion()
graph_centers_evolution()
graph_theta_omega()
graph_phase_diagram()
graph_energy()
