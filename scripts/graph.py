import matplotlib.pyplot as plt
from scripts.calculations import *
from scripts.variables import to_degrees
import os
import shutil
from datetime import datetime


# --- Creat graphs ---
def graph_motion_crane():
    """
    :return: Create the graph of the center of gravity as a function of time
    """
    plt.figure(1)
    plt.suptitle("Motion of the crane")
    plt.subplot(2, 1, 1)
    plt.plot(t, cg_x, label="Center of gravity - x")
    plt.xlabel("Time [s]")
    plt.ylabel("Position [m]")
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.plot(t, cg_z, label="Center of gravity - z")
    plt.xlabel("Time [s]")
    plt.ylabel("Position [m]")
    plt.legend()
    plt.figure(1).savefig('C:/Users/quent/PycharmProjects/Modelisation/graphs/motion_crane.png')
    plt.show()


def graph_centers_evolution():
    """
    :return: Draws a graph that shows the position of the center of gravity and thrust over time
    """
    plt.figure(2)
    plt.suptitle("Center of gravity and Center Thrust")
    plt.subplot(2, 1, 1)
    plt.plot(t, cp_x, label="Center Thrust - x")
    plt.plot(t, cg_x, '-r', label="Center of gravity - x")
    plt.xlabel("Time [s]")
    plt.ylabel("Position x [m]")
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.plot(t, cg_z, '-r', label="Center of gravity - z")
    plt.plot(t, cp_z, label="Center Thrust - z")
    plt.xlabel("Time [s]")
    plt.ylabel("Position z [m]")
    plt.legend()
    plt.figure(2).savefig('C:/Users/quent/PycharmProjects/Modelisation/graphs/centers_evolution.png')
    plt.show()


def graph_theta_omega():
    """
    :return: Create graphs for angle of inclination, angular velocity and angular acceleration as a function of time
    """
    plt.figure(3)
    plt.suptitle("ω and θ")

    plt.subplot(3, 1, 1)
    plt.plot(t, theta * to_degrees)
    plt.plot([0, t[-1]], [angle_submersion() * to_degrees, angle_submersion() * to_degrees], '--r', label="Submersion")
    plt.plot([0, t[-1]], [angle_elevation() * to_degrees, angle_elevation() * to_degrees], '--g',
             label="Elevation")
    plt.plot([0, t[-1]], [- angle_submersion() * to_degrees, - angle_submersion() * to_degrees], '--r')
    plt.plot([0, t[-1]], [- angle_elevation() * to_degrees, - angle_elevation() * to_degrees], '--g')
    plt.xlabel("Time [s]")
    plt.ylabel("θ [°]")
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(t, omega * to_degrees)
    plt.xlabel("Time [s]")
    plt.ylabel("ω [° / s]")

    plt.subplot(3, 1, 3)
    plt.plot(t, a * to_degrees)
    plt.xlabel("Time [s]")
    plt.ylabel("a [rad / s ** 2]")

    plt.figure(3).savefig('C:/Users/quent/PycharmProjects/Modelisation/graphs/theta_omega.png')
    plt.show()


def graph_phase_diagram():
    """
    :return: Creates a phase diagram
    """
    plt.figure(4)
    plt.title("Phase Diagram")
    plt.plot(theta * to_degrees, omega * to_degrees)
    plt.xlabel("θ [°]")
    plt.ylabel("ω [°/s]")
    plt.figure(4).savefig('C:/Users/quent/PycharmProjects/Modelisation/graphs/phase_diagram.png')
    plt.show()


def graph_energy():
    """
    :return: Creates the graphics of the energy (1 per energy)
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
    plt.figure(5).savefig('C:/Users/quent/PycharmProjects/Modelisation/graphs/energy_separate.png')
    plt.show()


def graph_energy_2():
    """
    :return: Creates the graphics of the energy (1 for all energy's)
    """
    plt.figure(6)
    plt.title("Energy")
    plt.plot(t, E_tot, label="Total Energy")
    plt.plot(t, E_p, label="Thrust Energy")
    plt.plot(t, E_g, label="Gravitational Energy")
    plt.plot(t, E_k, label="Kinetics Energy")
    plt.xlabel("Time [s]")
    plt.ylabel("Energy [J]")
    plt.legend()
    plt.figure(6).savefig('C:/Users/quent/PycharmProjects/Modelisation/graphs/energys.png')
    plt.show()


# --- Lunch program ---
# Save graphs
path_name = 'C:/Users/quent/PycharmProjects/Modelisation/graphs'
if os.path.isdir(path_name):
    shutil.rmtree(path_name)
os.mkdir(path_name)

graph_motion_crane()
graph_centers_evolution()
graph_theta_omega()
graph_phase_diagram()
graph_energy()
graph_energy_2()

# --- Print results and save it into a file ---
time = str(datetime.now())
table = str(tabulate([["Information's about", "Radians", "Degrees"],
                      ["Angle of submersion", angle_submersion(), angle_submersion() * to_degrees],
                      ["Angle of elevation", angle_elevation(), angle_elevation() * to_degrees],
                      ["Departure Inclination", theta[0], theta[0] * to_degrees],
                      ["Inclination before moving", theta[begin_motion * 10 - 1], theta[begin_motion * 10 - 1] * to_degrees],
                      ["Final Inclination", theta[-1], theta[-1] * to_degrees]],
                     headers="firstrow"))

with open('C:/Users/quent/PycharmProjects/Modelisation/graphs/results.txt', 'w') as file:
    file.write("Date : " + time + "\n \n" +
               "Simulation of the crane - group 11.57 \n"
               "===================================== \n \n"
               + table + "\n \n"
               "Submersion Height = {}m \n"
               "Counterweight : x : {}, z: {}".format(height_submersion(), counterweight_cg_x, counterweight_cg_z))
