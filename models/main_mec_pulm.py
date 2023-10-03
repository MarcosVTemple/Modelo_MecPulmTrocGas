from tqdm import tqdm
import pandas as pd
import numpy as np
import math as m
import time as t
import os

from parametros import cts_mp
from functions.derivada_mec_pulm import derivada_mp
from functions.entrada_mec_pulm import entrada_mp
from functions.saida_mec_pulm import saida_mp
from functions.plot_mec_pulm import plot_mp
from functions.controle_mec_pulm import controle_mp

from decorators.timefunc import timefunc


Cl = cts_mp["Cl"]
Ctr = cts_mp["Ctr"]
Ccw = cts_mp["Ccw"]
Cb = cts_mp["Cb"]
CA = cts_mp["CA"]

Rtb = cts_mp["Rtb"]
Rlt = cts_mp["Rlt"]
Rml = cts_mp["Rml"]
RbA = cts_mp["RbA"]

Vul = cts_mp["Vul"]
Vut = cts_mp["Vut"]
Vub = cts_mp["Vub"]
VuA = cts_mp["VuA"]
Ti = cts_mp["Ti"]
Te = cts_mp["Te"]
T = cts_mp["T"]
# Te = cts_mp["IEratio"]*Ti
tau = cts_mp["Te"]/5
RR = cts_mp["RR"]
IEratio = cts_mp["IEratio"]
f = RR/60
dt = cts_mp["dt"]
Pmus_min = cts_mp["Pmus_min"]
Pao = cts_mp["Pao"]
# Pvent = cts_mp["Pvent"]
Pvent = None

Pao_Pvent_zero = None
dPmus_zero = None
Pao_Pvent_zero = None
dPmus_zero = None

class MecanicaPulmonar:
    def __init__(self):
        tempo_simulacao = os.getenv("tempo_simulacao", default=None)
        if tempo_simulacao:
            cts_mp["N"] = int(int(tempo_simulacao)/cts_mp["dt"])
        
        Pl = np.zeros(cts_mp["N"], dtype=int)
        Ptr = np.zeros(cts_mp["N"], dtype=int)
        Pb = np.zeros(cts_mp["N"], dtype=int)
        PA = np.zeros(cts_mp["N"], dtype=int)
        Ppl = np.zeros(cts_mp["N"], dtype=int)
        vetor_zero = np.zeros(cts_mp["N"], dtype=int)
        
        Pao_Pvent_zero = np.zeros(cts_mp["N"], dtype=int)
        dPmus_zero = np.zeros(cts_mp["N"], dtype=int)
        Pao_Pvent_zero = np.zeros(cts_mp["N"], dtype=int)
        dPmus_zero = np.zeros(cts_mp["N"], dtype=int)
        
            
        self.t = np.arange(0, cts_mp["N"]*cts_mp["dt"], cts_mp["dt"])

        self.x_mp = pd.DataFrame(
            {
                'Pl': Pl, 'Ptr': Ptr, 'Pb': Pb, 'PA': PA, 'Ppl': Ppl
            }
        )
        self.y_mp = pd.DataFrame(
            {
                'V_dot': vetor_zero, 'VA_dot': vetor_zero, 'Vl': vetor_zero,
                'Vtr': vetor_zero, 'Vb': vetor_zero, 'VA': vetor_zero,
                'VD': vetor_zero, 'V': vetor_zero,
            }
        )
        self.u_mp = pd.DataFrame(
            {
                'dPmus': vetor_zero, 'Pao_Pvent': vetor_zero, 'Pmus': vetor_zero
            }
        )

    @timefunc
    def run_mecanica_pulmonar(self):
        self.inicializa_var_estado()
        self.rungekutta4()
        if os.getenv("save_data", default="") == 'TRUE':
            timestamp = str(int(round(t.time() * 1000)))
            self.x_mp.to_csv(f"temp/mp/data/variaveis_estado_dt_{dt}_{timestamp}.csv", sep=";", index=False)
            self.u_mp.to_csv(f"temp/mp/data/entradas_dt_{dt}_{timestamp}.csv", sep=";", index=False)
            # self.y_mp.to_csv(f"temp/mp/data/saidas_dt_{dt}_{timestamp}.csv", sep=";", index=False)
            self.y_mp.to_csv(f"temp/mp/data/saidas_dt_{dt}_{cts_mp['N']}.csv", sep=";", index=False)

    def inicializa_var_estado(self):
        """
            The initial conditions for the five different
            pressure nodes in Fig. 6 (state variables) have been assigned, assuming that at time t=0,
            corresponding to the end-exhalation time, all of the pressures in the lungs equilibrate to Patm,
            whereas the Ppl has a subatmospheric value of -5 cmH2O (72)
        """
        self.x_mp.iloc[0, 0] = Pao
        self.x_mp.iloc[0, 1] = Pao
        self.x_mp.iloc[0, 2] = Pao
        self.x_mp.iloc[0, 3] = Pao
        self.x_mp.iloc[0, 4] = -5

    def plot_mecanica_pulmonar(self):
        plot_mp(self.t, self.x_mp, self.y_mp, self.u_mp)

    def rungekutta4(self):
        RR_novo = None
        RR_inicial = cts_mp["RR"]
        RR = cts_mp["RR"]
        Pmus_min = cts_mp["Pmus_min"]
        tinicioT = 0
        tciclo_anterior = 0
        P_cap_O2 = 0
        P_cap_CO2 = 0
        
        tciclo, T, Te, Ti, RR, Pmus_min, tinicioT \
                = controle_mp(0, RR, IEratio, dt, P_cap_O2, P_cap_CO2, Pmus_min, tinicioT, tciclo_anterior)
                
        for i in tqdm(range(cts_mp["N"]-1)):   # iterations per second
            # u em t
            t = self.t[i]
            P_cap_O2 = 0
            P_cap_CO2 = 0
            V = self.y_mp.loc[i, "V"]
            
            RR = RR_novo if RR_novo else RR_inicial
            
            # u em t+dt
            t_dt = t + dt
            
            tciclo_dt, T_dt, Te_dt, Ti_dt, RR_dt, Pmus_min_dt, tinicioT_dt \
                = controle_mp(t_dt, RR, IEratio, dt, P_cap_O2, P_cap_CO2, Pmus_min, tinicioT, tciclo)

            u_t_array, Pmus \
                = entrada_mp(Pmus_min, Pao, tciclo, T, Te, Ti, Pvent)
                
            self.u_mp.loc[i, 'dPmus'] = u_t_array[0]
            self.u_mp.loc[i, 'Pao_Pvent'] = u_t_array[1]
            self.u_mp.loc[i, 'Pmus'] = Pmus
            u_t = np.matrix(u_t_array).transpose()

            u_dt_array, Pmus_dt \
                = entrada_mp(Pmus_min_dt, Pao, tciclo_dt, T_dt, Te_dt, Ti_dt, Pvent)
            u_dt = np.matrix(u_dt_array).transpose()

            # x em t
            x_array = self.x_mp.iloc[i, 0:].to_numpy()
            x = np.matrix(x_array).transpose()

            # constantes para RK2
            k1_rk2 = derivada_mp(x, u_t, Cl, Ctr, Ccw, Cb, CA, Rtb, Rlt, Rml, RbA)
            k2_rk2 = derivada_mp(x + k1_rk2*dt, u_dt, Cl, Ctr, Ccw, Cb, CA, Rtb, Rlt, Rml, RbA)

            # atribuindo os valores em x
            x_rk2 = x + dt*(k1_rk2+k2_rk2)/2  # RK2
            self.x_mp.iloc[i+1, :] = pd.DataFrame(x_rk2.transpose())

            # atribuindo os valores em y
            self.y_mp.iloc[i + 1, :] = saida_mp(x_rk2, u_t, Cl, Ctr, Cb, CA, Rtb, Rlt, Rml, RbA, Vul, Vut, Vub, VuA)
            VA_dot_mp = self.y_mp.iloc[i + 1, 1]


