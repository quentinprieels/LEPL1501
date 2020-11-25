import numpy as np
from tabulate import tabulate
from simple.variables import *
from math import sin, cos, tan, atan, pi

"""COORDINATE SYSTEM 
The following code takes place in a 3-dimensional coordinate system. However, some dimensions will be regularly ignored
(especially the Y component). A tuple with 2 coordinates is thus composed of the x-y coordinates. 
The X axis is horizontal (length) 
The Y-axis is horizontal (width)
he Z axis is vertical (height)
The origin is positioned in the middle of the barge along the X and Y axis and at water level along the Z axis. 
"""

# --- Simulation parameters ---
step = 0.01  # [s] steps (dt)
end = 100  # [s] duration
theta_0 = 0  # [rad] angle of inclination at t == 0
omega_0 = 0  # [rad / s] angular velocity at t == 0
begin_motion = 10  # [%] begin of motion (elapsed time)
end_motion = 50  # [%] end of motion (elapsed time)

# Lists with numpy
t = np.arange(0, end, step)  # [s] list of all times
theta = np.empty_like(t)  # [rad] list of all values of theta
omega = np.empty_like(t)  # [rad / s] list of all values of omega : the angular velocity
a = np.empty_like(t)  # [rad / s**2] list of all values of a : the angular acceleration
couples = np.empty_like(t)  # [N] list of all sum of torques

crane_cg_x = np.empty_like(t)
crane_cg_z = np.empty_like(t)

cg_x = np.empty_like(t)  # [m] All the position along the x-axis of the center of gravity
cg_z = np.empty_like(t)  # [m] All the position along the z-axis of the center of gravity
cp_x = np.empty_like(t)  # [m] All the position along the x-axis of the center of thrust
cp_z = np.empty_like(t)  # [m] All the position along the z-axis of the center of thrust
immersed_mass_values = np.empty_like(t)


# --- Moving of the crane ---
def motion():
    """
    Fill in the (movement) lists of the center of gravity of the crane according to time and percentage of duration.
    :return: True if there are no problem, otherwise False
    """
    try:
        # Lists with numpy
        crane_cg_x[0] = crane_cg_x_values[0]
        crane_cg_z[0] = crane_cg_z_values[0]

        # Start and end time of the movement
        motion_time = [int((len(t) / 100) * begin_motion), int((len(t) / 100) * end_motion)]

        # Steps
        step_crane_cg_x = (crane_cg_x_values[1] - crane_cg_x_values[0]) / (motion_time[1] - motion_time[0])
        step_crane_cg_z = (crane_cg_z_values[1] - crane_cg_z_values[0]) / (motion_time[1] - motion_time[0])

        # Fill lists
        for i in range(len(t) - 1):
            if motion_time[0] < i < motion_time[1]:
                crane_cg_x[i + 1] = crane_cg_x[i] + step_crane_cg_x
                crane_cg_z[i + 1] = crane_cg_z[i] + step_crane_cg_z
            else:
                crane_cg_x[i + 1] = crane_cg_x[i]
                crane_cg_z[i + 1] = crane_cg_z[i]

        return True
    except:
        return False


# --- Calculations ---
def rotate_coord(coord, angle):
    """
    This function applies a rotation to a couple of points x, y
    :type coord: tuple
    :type angle: float
    :param coord: The x, y coordinates of the point in R ** 2
    :param angle: The angle rotation IN RADIANS
    :return: a tuple witch is the coordinates pf the new point
    """
    x_prime = (cos(angle) * coord[0]) + (-sin(angle) * coord[1])
    y_prime = (sin(angle) * coord[0]) + (cos(angle) * coord[1])
    return tuple([x_prime, y_prime])


# --- Initial situation ---
def height_submersion():
    """ IT'S THE PARAMETER hc
    Calculate the submerged height of the barge
    :return: If hc < barge height : the distance hc (for height of submersion), where hc is the length follow the
    submerged z-axis of the barge. Otherwise, print that there is a problem en return None
    """
    hc = sum_mass / (1000 * barge_x * barge_y)  # [m]
    if 0 < hc < barge_z:
        return hc
    else:
        print("WARNING : hc >= barge z : the barge sinks")
        return None


def angle_submersion():
    """
    Calculate the angle of submersion of the barge. This is the angle beyond which water begins to come on the barge.
    :return: The value in radians of the angle of submersion (rotation around the y-axis).
    """
    # todo: The angle is defined as negative ?
    angle_submersion_value = - atan((barge_z - height_submersion()) / (barge_x / 2))  # [rad]
    if - pi / 2 < angle_submersion_value < pi / 2:
        return angle_submersion_value
    else:
        raise ValueError("WARNING : The angle of submersion is not between -pi / 2 and pi / 2")


def angle_elevation():
    """
    Calculate the angle of elevation of the barge. This is the angle at which a corner of the barge, which is nominally
    submerged, comes out of the water. (soulevement)
    :return: The value in radians of the angle of elevation (rotation around the y-axis).
    """
    angle_elevation_value = - atan(height_submersion() / (barge_x / 2))  # [rad]
    if - pi / 2 < angle_elevation_value < pi / 2:
        return angle_elevation_value
    else:
        raise ValueError("WARNING : The angle of elevation is not between -pi / 2 and pi / 2")


def center_gravity():
    """
    This function calculates the center of gravity of the whole system.
    FORMULA cg = sum of (mass_i * distance_(origin,point_i) / sum of mass_i
    :return: Fill the list of cg_x and cg_z
    """
    counter_problem = 0
    try:
        hc = height_submersion()
        hb = barge_z - hc
        for i in range(len(t)):
            barge_cg = (0, (barge_z / 2) - hc)
            crane_cg = (crane_cg_x[i], hb + crane_cg_z[i])
            counterweight_cg = (counterweight_cg_x, hb + counterweight_cg_z)

            cg_x[i] = ((crane_mass * barge_cg[0]) +
                       (crane_mass * crane_cg[0]) +
                       (counterweight_mass * counterweight_cg[0])) / sum_mass

            cg_z[i] = ((crane_mass * barge_cg[1]) +
                       (crane_mass * crane_cg[1]) +
                       (counterweight_mass * counterweight_cg[1])) / sum_mass

            counter_problem += 1

        return True

    except ZeroDivisionError:
        ZeroDivisionError("WARNING : Problem when calculating the center of gravity = ZeroDivision Value of i {}"
                          .format(counter_problem))
    except:
        raise ("WARNING : Problem when calculating the center of gravity. Value of i {}".format(counter_problem))


def center_thrust(angle):
    """
    Calculate the coordinate of the center of trust of the barge
    :type angle: float
    :param angle: The angle of inclination that the barge undergoes, changing the coordinate system and causing the
    submerged shape change. IN RADIANS
    :return: A tuple with the coordinate along X- and Z-axis of the center of trust
    """
    hc = height_submersion()

    # Slides S8 - Page 'Flotteur' where parallel_long = h1 and parallel_short = h2
    parallel_long = hc + abs((tan(angle) * (barge_x / 2)))
    parallel_short = hc - abs((tan(angle) * (barge_x / 2)))

    # Application formulas
    lctx = (barge_x * (parallel_long + (2 * parallel_short))) / \
           (3 * (parallel_long + parallel_long))
    lctz = ((parallel_long ** 2) + (parallel_long * parallel_short) + (parallel_short ** 2)) / \
           (3 * (parallel_long + parallel_long))

    # Coordinates in the inclined system
    ctx_rotate = (barge_z / 2) - lctx
    ctz_rotate = -(hc - lctz)  # It is underwater thus negative

    # Rotation of the system
    return rotate_coord((ctx_rotate, ctz_rotate), angle)


def immersed_mass(angle):
    """
    Calculate the mass of the volume of water displaced by the barge
    :type angle: float
    :param angle: the angle of inclination of the barge IN RADIANS
    :return: float that is the immersed mass
    """
    hc = height_submersion()
    parallel_long = hc + abs((tan(angle) * (barge_x / 2)))
    parallel_short = hc - abs((tan(angle) * (barge_x / 2)))

    trapeze_area = ((parallel_long + parallel_short) * barge_z) / 2
    sub_volume = trapeze_area * barge_y
    mass_im = sub_volume * 1000
    return mass_im


# --- Simulation ---
def simulation():
    """
    :return: Completes the omega, theta, a, cp_x and cp_z lists according to couples
    """
    motion()
    center_gravity()

    # Initial conditions
    dt = step
    omega[0] = omega_0
    theta[0] = theta_0

    for i in range(len(t) - 1):
        # Rotation center gravity
        cg_x[i] = rotate_coord((cg_x[i], cg_z[i]), theta[i])[0]
        cg_z[i] = rotate_coord((cg_x[i], cg_z[i]), theta[i])[1]

        # Torques
        couple_g = -sum_mass * g * cg_x[i]
        couple_p = immersed_mass(theta[i]) * g * center_thrust(theta[i])[0]
        couple_d = - damping * omega[i]
        couples[i] = couple_g + couple_p + couple_d

        # Angle, velocity and acceleration
        a[i] = couples[i] / inertia
        omega[i + 1] = omega[i] + a[i] * dt
        theta[i + 1] = theta[i] + omega[i] * dt

        # Fill lists
        immersed_mass_values[i] = immersed_mass(theta[i])
        cp_x[i] = center_thrust(theta[i])[0]
        cp_z[i] = center_thrust(theta[i])[1]

    immersed_mass_values[-1] = immersed_mass_values[-2]
    cp_x[1] = cp_x[2]
    cp_z[1] = cp_z[2]
    cp_x[-1] = cp_x[-2]
    cp_z[-1] = cp_z[-2]
    cg_x[-1] = cg_x[-2]
    cg_z[-1] = cg_z[-2]


# --- Lunch program and print results ---
simulation()
E_g = sum_mass * g * (cg_x - cg_x[0])
E_p = - immersed_mass_values * g * (cp_x - cp_x[0])
E_k = (inertia * omega ** 2) / 2

print("Simulation of the crane - group 11.57")
print("=====================================")
print()
print(tabulate([["Information's about", "Radians", "Degrees"],
                ["Angle of submersion", angle_submersion(), angle_submersion() * to_degrees],
                ["Angle of elevation", angle_elevation(), angle_elevation() * to_degrees],
                ["Departure Inclination", theta[0], theta[0] * to_degrees],
                ["Final Inclination", theta[-1], theta[-1] * to_degrees]],
               headers="firstrow"))
print()
print("Submersion Height = {}m".format(height_submersion()))
