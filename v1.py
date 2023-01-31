from typing import List

import pandas as pd
import numpy as np
import math as m
import matplotlib.pyplot as plt

from parametros import cts_mp


class MecanicaPulmonar:
    def __init__(self):
        self.t = np.arange(0, cts_mp["N"], cts_mp["dt"])

        RK_Q = np.zeros(cts_mp["N"], dtype=int)
        RK_dQ = np.zeros(cts_mp["N"], dtype=int)

        self.x = pd.DataFrame(
            {
                'RK_Q': RK_Q, 'RK_dQ': RK_dQ
            }
        )
        self.y = pd.DataFrame(
            {
                'Q_SAIDA': RK_Q, 'QA_SAIDA': RK_dQ, 'diff_Q_QA': RK_Q,
                'Paw': RK_dQ, 'PA': RK_Q,
            }
        )
        self.u_plot = pd.DataFrame(
            {
                'u': [], 'du': []
            }
        )

    def rungekutta4(self, cts_mp: dict):
        f = cts_mp["f"]
        Pfis = cts_mp["Pfis"]
        dt = cts_mp["dt"]
        for i in range(cts_mp["N"]-1):
            # u em t
            t = self.t[i]
            phi = 2 * m.pi * f * t
            u = self.get_entrada_mp(f, phi, Pfis)
            self.u_plot.append({"u": u[0], "du": u[1]}, ignore_index=True)

            # u em t+dt/2
            t_meio = ((self.t[i]+(self.t[i]+dt))/2)
            phi_meio = 2 * m.pi * f * t_meio
            u_meio = self.get_entrada_mp(f, phi_meio, Pfis)

            # u em t+dt
            t_dt = self.t[i] + dt
            phi_dt = 2 * m.pi * f * t_dt
            u_dt = self.get_entrada_mp(f, phi_dt, Pfis)

            x = self.x.iloc[i, 0:2].tolist()

            k1 = self.deriva_mp_rk(x, u[1], cts_mp)
            k2 = self.deriva_mp_rk(x + k1*dt/2, u_meio[1], cts_mp)
            k3 = self.deriva_mp_rk(x + k2*dt/2, u_meio[1], cts_mp)
            k4 = self.deriva_mp_rk(x + k3*dt, u_dt[1], cts_mp)

            self.x.iloc[i+1, 0] = x[0] + dt*(k1[0]+2*k2[0]+2*k3[0]+k4[0])/6
            self.x.iloc[i+1, 1] = x[1] + dt*(k1[1]+2*k2[1]+2*k3[1]+k4[1])/6

            # TO DO:
            # Y

            phi = phi_dt
            # PLOTS
        self.plot_data()

    @staticmethod
    def deriva_mp_rk(x, u, cts_mp) -> np.array:
        x1 = x[0]
        x2 = x[1]
        dx1 = x2
        dx2 = (-(1/cts_mp["Cl"])*x1 - ((cts_mp["Cs"]*cts_mp["Rc"]/cts_mp["Cl"])+cts_mp["Rp"]+cts_mp["Rc"])*x2 + u)/\
              (cts_mp["Rp"]*cts_mp["Rc"]*cts_mp["Cs"])
        return np.array([dx1, dx2])

    @staticmethod
    def get_entrada_mp(f: float, phi: float, Pfis: float) -> np.array:
        u_aux = Pfis * m.sin(phi)  # Pw
        u_der = 2 * m.pi * f * Pfis * m.cos(phi)  # dPw
        return np.array([u_aux, u_der])  # [mmHg]

    def plot_data(self):
        plt.figure()
        plt.title('Trajetória em x')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Posição (m)')
        plt.plot(self.t, np.array(self.x['RK_Q']), color='r', label='r(t)')
        plt.show()

    def run(self):
        self.rungekutta4(cts_mp)
        a = 0


if __name__ == "__main__":
    mec_pulm_obj = MecanicaPulmonar()
    mec_pulm_obj.run()
