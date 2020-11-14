import math
import numpy as np
import matplotlib.pyplot as plt


class Grue:  # on cree un objet grue
    def __init__(self, L_base, l_base, h_base, m_base, m_grue, d_cg_grue, inertie):  # différentes caractéristiques à rentrer lors de la creation de l'objet

        # on enregistre les caractéristique dans l'objet
        # base
        self.L_base = L_base
        self.l_base = l_base
        self.h_base = h_base
        self.m_base = m_base

        # grue
        self.m_grue = m_grue
        self.d_cg_grue = d_cg_grue

        # inertie
        self.I = inertie

        # on calcule l'enfoncement, le centre de gravité et les cas limites à partir des dimensions de la grue (ne dépend pas de la charge qu'on met) (voir modelisation)
        self.enfoncement = (m_base + m_grue) / (1000 * L_base * l_base)

        self.d_cg = (self.m_base * (self.h_base / 2 - self.enfoncement) + self.m_grue * (
                    d_cg_grue + self.h_base - self.enfoncement)) / (self.m_base + self.m_grue)

        self.update_theta_max()

        # on initialise la charge en disant qu'elle est au centre et qu'elle ne pèse rien
        self.d_c = 0
        self.m_c = 0

        # on initialise theta à 0 car la grue ne penche pas quand il n'y a pas de charge
        self.theta = 0

    ################################################################
    # Les actions qu'on peut faire avec la grue

    def charger(self, distance, masse):  # mettre une charge
        self.d_c = distance
        self.m_c = masse

    def update_theta(self):  # calculer le theta à l'equilibre pour la charge actuelle (voir modelisation)
        N = 12 * self.d_c * self.m_c * self.enfoncement
        D = self.L_base ** 2 * (self.m_base + self.m_grue + self.m_c) - 12 * self.enfoncement * self.d_cg * (
                    self.m_base + self.m_grue)

        theta = math.atan(N / D)

        self.theta = theta
        return theta

    def update_theta_max(self):  # calculer les thetas maximums (voir modelisation)
        self.theta_max = math.atan(2 * (self.h_base - self.enfoncement) / self.L_base), math.atan(
            2 * self.enfoncement / self.L_base)

        return self.theta_max

    ####simulation

    def calc_d_poussee(self, angle):  # calculer la coordonnées du centre de poussée pour un moment de la simulation (angle à l'instant i) (voir modelisation)
        return ((self.L_base ** 2) * math.tan(angle)) / (12 * self.enfoncement)

    def simuler(self, end, step, angle0=0, v0=0):  # calculer la simulation pour la charge actuelle
        """
        pre: end: le nb de secondes de la simulation, step: l'ecart entre deux calculs de mesure (en seconde), angle0: angle initial (0 si aucun angle est entré), v0: vitesse angulaire initiale (0 si aucun v entrée)

        post: remplit les tableaux pour la simulation
        """
        self.test = [0]

        g = 9.81
        D = 15  # coefficient d'amortissement

        dt = step

        # tableaux pour la simulation
        self.t = np.arange(0, end, step)  # points en x où on doit calculer a,v et angle

        # tableaux vides pour acceuillir les valeurs de a, v et angle au différent de t  ex: tq a[3]= accélération au temps t[3]
        self.angle = np.empty_like(self.t)
        self.v = np.empty_like(self.t)
        self.a = np.empty_like(self.t)

        # on met les valeurs initiales de la vitesse et l'angle
        self.v[0] = v0
        self.angle[0] = angle0

        for i in range(len(self.t) - 1):
            couple_poids = (self.d_cg * (self.m_base + self.m_grue) * g) * math.sin(self.angle[i])
            couple_charge = (self.d_c * self.m_c * g) * math.cos(self.angle[i])
            couple_poussee = -(self.m_c + self.m_base + self.m_grue) * g * self.calc_d_poussee(
                self.angle[i]) * math.cos(self.angle[i])

            couple_tot = couple_poids + couple_charge + couple_poussee - (self.v[i]) * D

            self.a[i] = couple_tot / self.I

            self.v[i + 1] = self.v[i] + self.a[i] * dt
            self.angle[i + 1] = self.angle[i] + self.v[i + 1] * dt
            self.a[i + 1] = self.a[i]

    def show_graphics(self, tolerance=0):  # on affiche les graphiques de la simulation

        # on affiche le graphique avec l'acceleration, la vitesse et l'angle
        plt.figure(1)
        plt.subplot(3, 1, 1)
        plt.plot(self.t, self.a, label="acceleration angulaire")
        plt.legend()

        plt.subplot(3, 1, 2)
        plt.plot(self.t, self.v, label="vitesse angulaire")
        plt.legend()

        plt.subplot(3, 1, 3)
        plt.plot(self.t, self.angle, label="angle")
        plt.legend()

        plt.show()

        # on affiche le graphique avec l'angle les cas limites, le theta à l'équilibre, le moment où on dépasse l'angle limite

        t_probleme = self.verif_t_probleme(tolerance)  # on verifie si il y a eu un probleme de submersion/soulevement

        if t_probleme:  # s'il y a eu un probleme, on affiche le graphe de l'angle en bleu avant le probleme et en gris apres
            maxi = max(self.angle)
            plt.plot([self.t[t_probleme], self.t[t_probleme]], [-maxi * 1.3, maxi * 1.3], color="orange",
                     label="Moment submersion/soulevement")

            plt.plot(self.t[:t_probleme + 1], self.angle[:t_probleme + 1], label="angle avant submersion/soulevement")
            plt.plot(self.t[t_probleme:], self.angle[t_probleme:], color="grey",
                     label="angle après submersion/soulevement")


        else:  # sinon, on affiche le graphe de l'angle totalement en bleu

            plt.figure(2)
            plt.plot(self.t, self.angle, label="angle")

        # on affiche les lignes des cas limites
        line_theta_final = np.full_like(self.t, self.update_theta())  # theta à l'équilibre calculé avec la modelisation

        plt.plot(self.t, line_theta_final, color="black")

        # submersion
        line_theta_max1_1 = np.full_like(self.t, self.theta_max[0])
        line_theta_max1_2 = np.full_like(self.t, -self.theta_max[0])

        plt.plot(self.t, line_theta_max1_1, color="red", label="submersion", linestyle="dashed")
        plt.plot(self.t, line_theta_max1_2, color="red", linestyle="dashed")

        # soulevement
        line_theta_max2_1 = np.full_like(self.t, self.theta_max[1])
        line_theta_max2_2 = np.full_like(self.t, -self.theta_max[1])

        plt.plot(self.t, line_theta_max2_1, color="purple", label="soulevement", linestyle="dashed")
        plt.plot(self.t, line_theta_max2_2, color="purple", linestyle="dashed")

        plt.legend()
        plt.show()

    def verif_t_probleme(self, tolerance=0):  # verifier si la grue a e-été submergée lors de la simulation

        for i in range(len(self.angle)):
            angle = self.angle[i]

            if abs(angle) + tolerance > min(self.theta_max):
                return i

        return False


###########################################################################

test = Grue(1, 1, 0.08, 20, 15, 0.2, 200)  # on cree une grue qui s'appelle test et qui est caractérisée par les valeurs entrées

test.charger(2, 1.5)  # on met une charge de 1.5 kg à une distance de 2m

test.simuler(150, 0.01)  # on simule les 150 sec après avoir mis la charge en calculant un point toutes les 0.01 sec

test.show_graphics()  # on affiche les graphes
"""
test2 = Grue(0.5, 0.5, 0.1, 3, 1.05, 0.01, 0.5)
test2.charger(0.4, 0.1)
test2.simuler(60, 0.01)
test2.show_graphics()
"""