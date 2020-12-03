from scripts.variables import *
from math import sqrt, sin, cos, e
import matplotlib.pyplot as plt
import numpy as np
from scripts.calculations import height_submersion, cg_x

# Time
step = 0.01
end = 10
time = np.arange(0, end, step)

# Variables
theta = []
hc = height_submersion()
D = damping
L = barge_x
I = inertia
K = ((1000 * (L ** 2)) / 6) * g * 3 * hc

for t in range(len(time)):
    theta.append(0)
    U = sum_mass * g * cg_x[t] + ((1000 * (L ** 3) * g) / 12)
    w = (sqrt((4 * I * U) - (D ** 2))) / 2 * I
    theta[t] = (e ** ((-D) / (2 * I) * t)) * ((-K / U) * cos(w * t) - ((D * K) / (2 * U * I * w)) * sin(w * t)) + (K / U)
    theta[t] *= to_degrees

# Graph
plt.figure(1)
plt.title("On y croit Seb")
plt.plot(time, theta, label="Angle d'inclinaison")
plt.ylabel("Angle [?]")
plt.xlabel("Temps [s]")
plt.legend()
plt.show()
