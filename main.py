import numpy as np
from math import atan, cos, sin, tan
from variables import *

"""COORDINATE SYSTEM 
The following code takes place in a 3-dimensional coordinate system. However, some dimensions will be regularly ignored
(especially the Y component). A tuple with 2 coordinates is thus composed of the x-y coordinates. 
The X axis is horizontal (length) 
The Y-axis is horizontal (width)
he Z axis is vertical (height)
The origin is positioned in the middle of the barge along the X and Y axis and at water level along the Z axis. 
"""

# --- Simulation parameters ---
step = 0.1  # [s] steps (dt)
end = 100  # [s] duration
theta_0 = 0  # [rad] angle of inclination at t == 0
omega_0 = 0  # [rad / s] angular velocity at t == 0

t = np.arange(0, end, step)
theta = np.empty_like(t)
omega = np.empty_like(t)
couples = np.empty_like(t)
a = np.empty_like(t)
cg_list_x = []
cg_list_z = []

# --- Moving of the crane ---
grue2_angle = np.empty_like(t)  # [rad] angle from horizontal of the 2 crane part
grue3_angle = np.empty_like(t)  # [rad] angle from horizontal of the 3 crane part
grue3_x = np.empty_like(t)  # [m] length of the 3 crane part
grue4_angle = np.empty_like(t)  # [rad] angle from horizontal of the 4 crane part
begin_motion = 10  # [%] begin of motion (elapsed time)
end_motion = 50  # [%] end of motion (elapsed time)


def motion_list():
    """
    Fill in the movement lists according to time and percentage of duration.
    :return: True if all is ok, otherwise False
    """
    try:
        # Begin value
        grue2_angle[0] = grue2_angle_value[0]
        grue3_angle[0] = grue3_angle_value[0]
        grue3_x[0] = grue3_x_value[0]
        grue4_angle[0] = grue4_angle_value[0]

        # Motion
        motion = [int((len(t) / 100) * begin_motion), int((len(t) / 100) * end_motion)]

        # Step
        step_grue2_angle = (grue2_angle_value[1] - grue2_angle_value[0]) / (motion[1] - motion[0])
        step_grue3_angle = (grue3_angle_value[1] - grue3_angle_value[0]) / (motion[1] - motion[0])
        step_grue3_x = (grue3_x_value[1] - grue3_x_value[0]) / (motion[1] - motion[0])
        step_grue4_angle = (grue4_angle_value[1] - grue4_angle_value[0]) / (motion[1] - motion[0])

        # Fill lists
        for i in range(len(t) - 1):
            if motion[0] < i < motion[1]:
                grue2_angle[i + 1] = grue2_angle[i] + step_grue2_angle
                grue3_angle[i + 1] = grue3_angle[i] + step_grue3_angle
                grue3_x[i + 1] = grue3_x[i] + step_grue3_x
                grue4_angle[i + 1] = grue4_angle[i] + step_grue4_angle
            else:
                grue2_angle[i + 1] = grue2_angle[i]
                grue3_angle[i + 1] = grue3_angle[i]
                grue3_x[i + 1] = grue3_x[i]
                grue4_angle[i + 1] = grue4_angle[i]

        return True
    except:
        return False


# --- Initial situation and Calculations ---
def height_submersion():
    """
    Calculate the submerged height of the barge
    :return: If hc < barge height : the distance hc (for height of submersion), where hc is the length follow the
    submerged z-axis of the barge. Otherwise, None
    """
    hc = mass_sum / (1000 * (barge_x * barge_y))
    if hc < barge_z:
        return hc
    else:
        return None


def maximum_inclination():
    """
    This function calculates the maximum tilt angles before the barge sinks along the X-axis.
    :return: The value in radians of the angle along the X-axis.
    """
    try:
        # Fist method
        tan_theta = (barge_z - height_submersion()) / (barge_x / 2)
        angle_max = atan(tan_theta)

        return angle_max

    except:
        print("Problem when calculating the maximum tilt angle")
        return None


def center_gravity(*args):
    """
        This function calculates the center of gravity of a set of n bodies.
        Each of these bodies has 2 coordinates (one x and one y). The system is thus in 2 dimensions.
        The formula that is use is : cg(x) = ( m1*d1(x) + m2*d2(x) + m3*d3(x) + ...) / (m1 + m2 + m3 + ...)
        (same form for the y axes).
        :type args: tuple
        :param args: Each argument is a tuple of values. They are of the form (mass, (x-coordinate, y-coordinate)).
        :return: A tuple witch the Coordinates in the form (x-coordinate, y-coordinate) of the center of gravity.
        If the calculation is impossible, return None
        """
    sum_of_mass = 0
    for m in args:
        sum_of_mass += m[0]

    nominator_x = 0
    nominator_y = 0
    for x in args:
        mass_dist_x = x[0] * x[1][0]
        nominator_x += mass_dist_x
    for y in args:
        mass_dist_y = y[0] * y[1][1]
        nominator_y += mass_dist_y

    try:
        cgx = nominator_x / sum_of_mass
        cgy = nominator_y / sum_of_mass
        return tuple([cgx, cgy])

    except ZeroDivisionError:
        print("Mass of the null system, no value for the center of gravity")
        return None


def rotate_coord(coord, angle):
    """
    This function applies a rotation to a couple of points x, y
    :type coord: tuple
    :type angle: float IN RADIAN
    :param coord: The x, y coordinates of the point in R ** 2
    :param angle: The angle rotation
    :return: a tuple witch is the coordinates pf the new point
    """
    x_prime = (cos(angle) * coord[0]) + (-sin(angle) * coord[1])
    y_prime = (sin(angle) * coord[0]) + (cos(angle) * coord[1])
    return tuple([x_prime, y_prime])


# --- Information's about the crane in function of the time ---
def end_crane(index):
    """
    This function calculates the end of the crane as a function of time.
    :type index: int
    :param index: This is the index in the 'np' lists of time. These lists have been completed by the function
    motion_list()
    :return:  A tuple that is the coordinate along the x and z axis of the end of the crane
    """
    hb = (barge_z / 2) - height_submersion()
    end_crane_init = (((cos(grue2_angle[index]) * grue2_x) + (cos(grue3_angle[index]) * grue3_x[index]) + grue4_x),
                      (grue1_x + hb + (sin(grue2_angle[index]) * grue2_x) + (
                              sin(grue3_angle[index]) * grue3_x[index]) + grue4_z))
    return rotate_coord(end_crane_init, grue4_angle[index])


def global_center_gravity(index):
    """
    This function calculates the coordinates of the center of gravity of the whole crane as a function of time.
    :type index: int
    :param index: This is the index in the 'np' lists of time. These lists have been completed by the function
    motion_list()
    :return: A tuple that is the coordinate along the x and z axis of the center of gravity
    """
    # -- Barge --
    hc = height_submersion()
    hb = (barge_z / 2) - hc
    barge_cg = (0, hb)

    # -- Grue --
    # First Piece
    grue1_cg = (0, hb + (grue1_z / 2))

    # Second Piece
    grue2_cg_init = ((grue2_x / 2), (hb + grue1_x + (grue2_z / 2)))
    grue2_cg = rotate_coord(grue2_cg_init, grue2_angle[index])

    # Third Piece
    grue3_cg_init = (((cos(grue2_angle[index]) * grue2_x) + (grue3_x[index] / 2)),
                     (grue1_x + hb + (sin(grue2_angle[index]) * grue2_x) + (grue3_z / 2)))
    grue3_cg = rotate_coord(grue3_cg_init, grue3_angle[index])

    # Fourth Piece
    grue4_cg_init = (((cos(grue2_angle[index]) * grue2_x) + (cos(grue3_angle[index]) * grue3_x[index]) + (grue4_x / 2)),
                     (grue1_x + hb + (sin(grue2_angle[index]) * grue2_x) + (sin(grue3_angle[index]) * grue3_x[index]) +
                      (grue4_z / 2)))
    grue4_cg = rotate_coord(grue4_cg_init, grue4_angle[index])

    # -- Syringes --
    # todo: there are now negligees

    # -- Windturbine -- = Coordinates of the end of part 3 of the crane
    windturbine_cg = end_crane(index)

    # -- Counterweight --
    counterweight_position_z = barge_z - hc
    counterweight_cg = (counterweight_position_x + (counterweight_x / 2),
                        counterweight_position_z + (counterweight_y / 2))

    # Center of gravity
    cg = center_gravity((barge_mass, barge_cg),
                        (grue1_mass, grue1_cg),
                        (grue2_mass, grue2_cg),
                        (grue3_mass, grue3_cg),
                        (grue4_mass, grue4_cg),
                        (windturbine_mass + grapple_mass, windturbine_cg),
                        (counterweight_mass, counterweight_cg))

    return cg


def center_thrust(angle):
    """
    Calculate the coordinate of the center of trust of the barge
    :type angle: float
    :param angle: The angle of inclination that the barge undergoes, changing the coordinate system and causing the
    submerged shape change.
    :return: A tuple with the coordinate along X- and Z-axis of the center of trust
    """
    hc = height_submersion()

    # - The coordinate system also rotates -
    """ Formulas
    lxc = lctx = ( l * (h1 + 2 * h2) ) / (3 * (h1 + h2) )
    hc = lctz = (h1 ** 2 + h1 * h2 + h2 ** 2) / (3 * (h1 + h2) )
    Where :
     -  l = barge_x
     - h1 = parallel_right 
     - h2 = parallel_left 
       => the trapeze is in the wrong direction in the slides
    """
    # Length of the 2 parallel sides of the trapeze
    parallel_left = (hc + (tan(angle) * (barge_x / 2)))
    parallel_right = (hc - (tan(angle) * (barge_x / 2)))

    # Application of formulas
    lctx = (barge_x / 3) * ((parallel_right + (2 * parallel_left)) / (parallel_right + parallel_left))
    lctz = ((parallel_right ** 2) + (parallel_right * parallel_left) + (parallel_left ** 2)) / (
            3 * (parallel_right + parallel_left))

    # Coordinates in the inclined system
    ctx_rotate = (barge_x / 2) - lctx
    ctz_rotate = hc - lctz

    # - Rotation of the system -
    return rotate_coord((ctx_rotate, ctz_rotate), angle)

    """
    ctx = (ctx_rotate * cos(angle)) + (ctz_rotate * -sin(angle))
    ctz = (ctx_rotate * sin(angle)) + (ctz_rotate * cos(angle))
    return tuple([ctx, ctz])
    """


def immersed_mass(angle):
    """
    Calculate the mass of the volume of water displaced by the barge
    :type angle: float
    :param angle: the angle of inclination of the barge
    :return: float
    """
    hc = height_submersion()
    # Length of the 2 parallel sides of the trapeze
    parallel_left = (hc - (tan(angle) * (barge_x / 2)))
    parallel_right = (hc + (tan(angle) * (barge_x / 2)))

    trapeze_area = ((parallel_left + parallel_right) * barge_z) / 2
    sub_volume = trapeze_area * barge_y
    mass_im = sub_volume * 1000
    return mass_im


# --- Angles ---
def simulation():
    # Initial conditions
    dt = step
    omega[0] = omega_0
    theta[0] = theta_0

    for k in range(len(t) - 1):
        couple_g = -mass_sum * g * global_center_gravity(k)[0]
        couple_p = immersed_mass(theta[k]) * g * center_thrust(theta[k])[0]
        couple_d = -D * omega[k]
        couples[k] = couple_g + couple_p + couple_d

        a[k] = couples[k] / inertia
        omega[k + 1] = omega[k] + a[k] * dt
        theta[k + 1] = theta[k] + omega[k] * dt
        a[k + 1] = a[k]

        # print("{} \t CG = {} \t CP = {} \t CD = {} \t T = {}".format(k, couple_g, couple_p, couple_d, theta[k]))
        # print("{} \t {} \t {}".format(k, immersed_mass(theta[k]), center_thrust(theta[k])))


# --- Lunch program ---
motion_list()
simulation()

for i in range(len(t)):
    cg_list_x.append(global_center_gravity(i)[0])
    cg_list_z.append(global_center_gravity(i)[1])
