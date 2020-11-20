import matplotlib.pyplot as plt
from simple.calculations import *
from simple.variables import to_degrees


# --- Creat graphs ---
def graph_centers_evolution():
    """
    :return: Draws a graph that shows the position of the center of gravity and thrust over time
    """
    plt.figure(2)
    plt.suptitle("Center of gravity and Center Thrust")
    plt.subplot(2, 1, 1)
    plt.plot(t, cg_x, '-r', label="Center of gravity - x")
    plt.plot(t, cp_x, label="Center Thrust - x")
    plt.xlabel("Time [s]")
    plt.ylabel("Position x [m]")
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.plot(t, cg_z, '-r', label="Center of gravity - z")
    plt.plot(t, cp_z, label="Center Thrust - z")
    plt.xlabel("Time [s]")
    plt.ylabel("Position z [m]")
    plt.legend()
    plt.show()


def graph_theta_omega():
    plt.figure(3)
    plt.suptitle("ω and θ")

    plt.subplot(3, 1, 1)
    plt.plot(t, theta * to_degrees)
    plt.plot([0, t[-1]], [angle_submersion() * to_degrees, angle_submersion() * to_degrees], '--r',
             label="Submersion")
    plt.plot([0, t[-1]], [angle_elevation() * to_degrees, angle_elevation() * to_degrees], '--g',
             label="Elevation")
    plt.plot([0, t[-1]], [- angle_submersion() * to_degrees, - angle_submersion() * to_degrees], '--r',
             label="Submersion")
    plt.plot([0, t[-1]], [- angle_elevation() * to_degrees, - angle_elevation() * to_degrees], '--g',
             label="Elevation")
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

    plt.legend()

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
graph_centers_evolution()
graph_theta_omega()
graph_phase_diagram()
graph_energy()
