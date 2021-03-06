from math import pi

# --- Constants ---
inertia = 0.5202  # [kg * m**2] Inertia
g = 9.81  # [m / s**2] Gravitational acceleration
damping = 1.2  # [#] Damping of the system
to_degrees = 180 / pi  # [#] coefficient to transform rad in degrees
to_radians = pi / 180  # [#] coefficient to transform degrees in rad

# --- Barge ---
barge_x = 0.55  # [m] Barge length
barge_y = 0.60  # [m] Barge width
barge_z = 0.17  # [m] Barge height
barge_mass = 4.3  # [kg] Barge mass
barge_cg_values = (-0.095, 0.140)  # [m] Center of gravity of the barge with the wood planks

# --- Crane --- (Grapple, syringes and 3D printed parts are also considered)
""" COORDINATES SYSTEM
The origin of this coordinate system is located in the middle of the bottom of the crane base.
"""
crane_mass = 1.8  # [kg] Mass of all this components
# - Determinate with Fusion360 -
crane_cg_x_values = (0.069, 0.458)  # [m] Values along the x-axis of the center of gravity of all components (
# initial, final) (0.069, 0.248)
crane_cg_z_values = (0.251, 0.257)  # [m] Values along the y-axis of the center of gravity of all
# components (initial, final)

# --- Counterweight ---
""" COORDINATES SYSTEM
The origin of this coordinate system is located in the middle of the bottom of the crane base.
"""
counterweight_mass = 2  # [kg] Counterweight mass
counterweight_cg_x = -0.2  # [m] Values along the x-axis of the center of gravity of the counterweight
counterweight_cg_z = -0.15  # [m] Values along the z-axis of the center of gravity of the counterweight

# --- Total ---
sum_mass = barge_mass + crane_mass + counterweight_mass
