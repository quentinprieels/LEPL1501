from math import pi

# -- Others --
inertia = 1  # [kg.m**2]Inertia
g = 9.81  # [m / s**2] Gravitational acceleration
D = 1  # todo: what is this ?
to_degrees = 180 / pi  # [#] coefficient to transform rad in degrees
to_radians = pi / 180  # [#] coefficient to transform degrees in rad


# -- Barge --
barge_x = 0.5  # [m] Barge length
barge_y = 0.5  # [m] Barge width
barge_z = 0.08  # [m] Barge height
barge_mass = 5  # [kg] Barge mass


# -- Grue --
# - First Piece -
grue1_x = 0.15  # [m] Grue First Piece length
grue1_z = 0.05  # [m] Grue First Piece height
grue1_mass = 0.05  # [kg] Grue First Piece mass
# Grue First Piece angle is always 0

# - Second Piece -
grue2_x = 0.350  # [m] Grue Second Piece length
grue2_z = 0.05  # [m] Grue Second Piece height
grue2_mass = 0.35  # [kg] Grue Second Piece mass
grue2_angle_value = [81 * to_radians, 42 * to_radians]  # [deg] Angle of departure and arrival of this piece
# of grue. These angles are expressed as a function of the horizontal

# - Third Piece -
grue3_x_value = [0.3, 0.4]  # [m] Grue Third Piece start and finish length
grue3_z = 0.05  # [m] Grue Third Piece height
grue3_mass = 0.6  # [kg] Grue Third Piece mass
grue3_angle_value = [(-70) * to_radians, 4 * to_radians]  # [deg] Angle of departure and arrival of this piece of
# grue. These angles are expressed as a function of the horizontal

# - Fourth Piece -
grue4_x = 0.1  # [m] Grue Fourth Piece height
grue4_z = 0.05  # [m] Grue Fourth Piece height
grue4_mass = 0.05  # [kg] Grue Fourth Piece mass
grue4_angle_value = [(-90) * to_radians, 0 * to_radians]  # [deg] Angle of departure and arrival of this piece
# of grue. These angles are expressed as a function of the horizontal


# -- Grapple --
grapple_mass = 0.1  # [kg] Mass of the grapple


# -- Syringes --
#  todo: there are now negligees


# -- Windturbine --
windturbine_mass = 0.1  # [kg] Windturbine mass
# The size of the turbine is not taken in consideration. It is considered to be in the grapple at all times.


# -- Counter-weight --
counterweight_x = 0.1  # [m] Counterweight length
counterweight_position_x = - 0.1  # [m] Position along the x-axis of the counterweight
counterweight_y = 0.1  # [m] Counterweight width
counterweight_z = 0  # [m] Counterweight height
counterweight_mass = 7.5  # [kg] Counterweight mass


# -- Calculations --
mass_sum = barge_mass + grue1_mass + grue2_mass + grue3_mass + grue4_mass + grapple_mass + windturbine_mass + \
           counterweight_mass
