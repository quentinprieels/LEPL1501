from math import pi


# --- Constants ---
inertia = 0.152  # [kg * m**2] Inertia
g = 9.81  # [m / s**2] Gravitational acceleration
damping = 1  # [ ? ] Damping of the system
to_degrees = 180 / pi  # [#] coefficient to transform rad in degrees
to_radians = pi / 180  # [#] coefficient to transform degrees in rad


# --- Barge ---
barge_x = 0.55  # [m] Barge length
barge_y = 0.6  # [m] Barge width
barge_z = 0.15  # [m] Barge height
barge_mass = 5  # [kg] Barge mass


# --- Crane --- (Grapple, syringes and 3D printed parts are also taken into account)
""" COORDINATES SYSTEM
The origin of this coordinate system is located in the middle of the bottom of the crane base.
"""
crane_mass = 1.73  # [kg] Mass of all this components
# - Determinate with Fusion360 -
crane_cg_x_values = (0.083423, 0.271)  # [m] Values along the x-axis of the center of gravity of all components (
# initial, final)
crane_cg_z_values = (0.266024, 0.229)  # [m] Values along the y-axis of the center of gravity of all components (
# initial, final)

# -- Test with difference mass --
# test_cane = (mass, (cg_x_ini, cg_x_final), (cg_z_init, cg_z_final))
test_crane_100 = (1.83, (0.100, 0.297), (0.267, 0.235))
test_crane_200 = (1.93, (0.117, 0.321), (0.268, 0.240))
test_crane_500 = (2.23, (0.156, 0.378), (0.271, 0.253))
test_crane_700 = (2.43, (0.177, 0.408), (0.272, 0.259))


# --- Counterweight ---
""" COORDINATES SYSTEM
The origin of this coordinate system is located in the middle of the bottom of the crane base.
"""
counterweight_mass = 3  # [kg] Counterweight mass
counterweight_cg_x = -0.2  # [m] Values along the x-axis of the center of gravity of the counterweight
counterweight_cg_z = -0.15  # [m] Values along the z-axis of the center of gravity of the counterweight


# --- If necessary ---
# WARNING: is not taken into account in the calculation of the center of gravity (nominator of fraction)
other_mass = 0


# --- Total ---
sum_mass = barge_mass + crane_mass + counterweight_mass + other_mass
