from tqdm import tqdm
import pandas as pd
import numpy as np
import math as m
import time as t
import os

from parametros import cts_mp, cts_tg, cts_int
from funcoes.plot_integracao import plot_int
from funcoes.controle_mec_pulm import controle_mp

from funcoes.entrada_troc_gas import entrada_tg
from funcoes.derivada_troc_gas import derivada_tg
from funcoes.saida_troc_gas import saida_tg
from funcoes.plot_troc_gas import plot_tg

from parametros import cts_mp
from funcoes.derivada_mec_pulm import derivada_mp
from funcoes.entrada_mec_pulm import entrada_mp
from funcoes.saida_mec_pulm import saida_mp
from funcoes.plot_mec_pulm import plot_mp

from decorators.timefunc import timefunc

RR = cts_tg["RR"]
dt = cts_int["dt"]
Pfis = cts_tg["Pfis"]
f = RR / 60

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
# Ti = cts_mp["Ti"]
# Te = cts_mp["Te"]
T = cts_mp["T"]
# Te = cts_mp["IEratio"]*Ti
tau = cts_mp["Te"]/5
RR = cts_mp["RR"]
IEratio = cts_mp["IEratio"]
f = RR/60

Pmus_min = cts_mp["Pmus_min"]
Pao = cts_mp["Pao"]
# Pvent = cts_mp["Pvent"]
Pvent = None

Pao_Pvent_zero = None
dPmus_zero = None
Pao_Pvent_zero = None
dPmus_zero = None

# int 
dt = cts_int["dt"]


class Integracao:
    def __init__(self):
        tempo_simulacao = os.getenv("tempo_simulacao", default=None)
        if tempo_simulacao:
            cts_int["N"] = int(int(tempo_simulacao)/cts_int["dt"])

        # mp
        Pl = np.zeros(cts_int["N"], dtype=int)
        Ptr = np.zeros(cts_int["N"], dtype=int)
        Pb = np.zeros(cts_int["N"], dtype=int)
        PA = np.zeros(cts_int["N"], dtype=int)
        Ppl = np.zeros(cts_int["N"], dtype=int)
        vetor_zero = np.zeros(cts_int["N"], dtype=int)
        
        Pao_Pvent_zero = np.zeros(cts_int["N"], dtype=int)
        dPmus_zero = np.zeros(cts_int["N"], dtype=int)
        Pao_Pvent_zero = np.zeros(cts_int["N"], dtype=int)
        dPmus_zero = np.zeros(cts_int["N"], dtype=int)
        
            
        self.t = np.arange(0, cts_int["N"]*cts_mp["dt"], cts_mp["dt"])

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

        # tg
        n_A_O2 = np.zeros(cts_int["N"], dtype=int)
        n_A_CO2 = np.zeros(cts_int["N"], dtype=int)
        n_A_N2 = np.zeros(cts_int["N"], dtype=int)
        n_cap_O2 = np.zeros(cts_int["N"], dtype=int)
        n_cap_CO2 = np.zeros(cts_int["N"], dtype=int)
        n_cap_N2 = np.zeros(cts_int["N"], dtype=int)
        n_t_O2 = np.zeros(cts_int["N"], dtype=int)
        n_t_CO2 = np.zeros(cts_int["N"], dtype=int)
        n_t_N2 = np.zeros(cts_int["N"], dtype=int)
        P_A_O2 = np.zeros(cts_int["N"], dtype=int)
        P_A_CO2 = np.zeros(cts_int["N"], dtype=int)
        P_A_N2 = np.zeros(cts_int["N"], dtype=int)
        P_cap_O2 = np.zeros(cts_int["N"], dtype=int)
        P_cap_CO2 = np.zeros(cts_int["N"], dtype=int)
        P_cap_N2 = np.zeros(cts_int["N"], dtype=int)
        VA_dot = np.zeros(cts_int["N"], dtype=int)

        self.entrada_tg_from_mp = None
        self.t = np.arange(0, cts_int["N"] * cts_int["dt"], cts_int["dt"])
        self.x_tg = pd.DataFrame(
            {
                'n_A_O2': n_A_O2, 'n_A_CO2': n_A_CO2, 'n_A_N2': n_A_N2,
                'n_cap_O2': n_cap_O2, 'n_cap_CO2': n_cap_CO2,
                'n_t_O2': n_t_O2, 'n_t_CO2': n_t_CO2
            }
        )
        self.y_tg = pd.DataFrame(
            {
                'P_A_O2': P_A_O2,
                'P_A_CO2': P_A_CO2,
                'P_A_N2': P_A_N2,
                'P_cap_O2': P_cap_O2,
                'P_cap_CO2': P_cap_CO2,
            }
        )
        self.u_tg = pd.DataFrame(
            {
                'VA_dot': VA_dot,
            }
        )

    def inicializa_var_estado(self):
        # mp
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
        
        # tg
        nt_inicial = ((cts_tg["Patm"]*cts_tg["VA_t"])/(cts_tg["R"]*cts_tg["Temp"]))*1000
        self.x_tg.iloc[0, 0] = nt_inicial*cts_tg["f_O2"]  # 6.7145
        self.x_tg.iloc[0, 1] = nt_inicial*cts_tg["f_CO2"]  # 2.5817
        self.x_tg.iloc[0, 2] = nt_inicial*cts_tg["f_N2_H2O"]

        self.x_tg.iloc[0, 3] = 0.535#0.5388
        self.x_tg.iloc[0, 4] = 0.23#0.2072

        self.x_tg.iloc[0, 5] = 150#181.56
        self.x_tg.iloc[0, 6] = 100 #85.23
        # self.entrada_tg_from_mp = pd.read_csv(f"results/mp/data/saidas_dt_0.0004_{cts_mp['N']}.csv", sep=";")['VA_dot']
        # self.entrada_tg_from_mp = pd.read_csv(f"results/mp/data/saidas_dt_0.0004_{500000}.csv", sep=";")['VA_dot']
        
    def plot_integracao(self):
        plot_int(self.t, self.x_tg, self.y_tg, self.u_tg, self.x_mp, self.y_mp, self.u_mp)
        
    @timefunc
    def run_integracao(self):
        self.inicializa_var_estado()
        self.rungekutta4()
        
        # mp
        if os.getenv("save_data", default="") == 'TRUE':
            timestamp = str(int(round(t.time() * 1000)))
            self.x_mp.to_csv(f"results/mp/data/variaveis_estado_dt_{dt}_{timestamp}.csv", sep=";", index=False)
            self.u_mp.to_csv(f"results/mp/data/entradas_dt_{dt}_{timestamp}.csv", sep=";", index=False)
            # self.y_mp.to_csv(f"results/mp/data/saidas_dt_{dt}_{timestamp}.csv", sep=";", index=False)
            self.y_mp.to_csv(f"results/mp/data/saidas_dt_{dt}_{cts_mp['N']}.csv", sep=";", index=False)
        
        # tg
        if os.getenv("save_data", default="") == 'TRUE':
            timestamp = str(int(round(t.time() * 1000)))
            self.x_tg.to_csv(
                f"results/tg/data/troca_gases_variaveis_estado_dt_{dt}_{cts_tg['modo_ventilacao']}_{timestamp}.csv",
                sep=";",
                index=False
            )
            self.y_tg.to_csv(
                f"results/tg/data/troca_gases_saidas_dt_{dt}_{cts_tg['modo_ventilacao']}_{timestamp}.csv",
                sep=";",
                index=False
            )
            
    def rungekutta4(self):
        RR = cts_mp["RR"]
        RR_calculado = None
        Pmus_min = cts_mp["Pmus_min"]
        Pmus_min_calculado = None
        tinicioT = 0
        tinicioT_calculado = None
        P_cap_O2 = self.y_tg.loc[0, "P_cap_O2"]
        P_cap_CO2 = self.y_tg.loc[0, "P_cap_CO2"]
        
        tciclo, T, Te, Ti, RR, Pmus_min, tinicioT \
                = controle_mp(0, RR, IEratio, dt, P_cap_O2, P_cap_CO2, Pmus_min, tinicioT)
        
        for i in tqdm(range(cts_int["N"]-1)):
            ### mp
            
            # u em t
            t = self.t[i]

            
            # if t > 0:
            #     RR = RR_calculado
            #     Pmus_min = Pmus_min_calculado
            #     tinicioT = tinicioT_calculado
            
            # tciclo, T, Te, Ti, RR_calculado, Pmus_min_calculado, tinicioT_calculado \
            #     = controle_mp(t, RR, IEratio, dt, P_cap_O2, P_cap_CO2, Pmus_min, tinicioT)
            
            u_t_array, Pmus \
                = entrada_mp(Pmus_min, Pao, tciclo, T, Te, Ti, Pvent)
                
            self.u_mp.loc[i, 'dPmus'] = u_t_array[0]
            self.u_mp.loc[i, 'Pao_Pvent'] = u_t_array[1]
            self.u_mp.loc[i, 'Pmus'] = Pmus
            u_t = np.matrix(u_t_array).transpose()

            # u em t+dt
            t_dt = t + dt
            
            tciclo_dt, T_dt, Te_dt, Ti_dt, RR_dt, Pmus_min_dt, tinicioT_dt \
                = controle_mp(t_dt, RR, IEratio, dt, P_cap_O2, P_cap_CO2, Pmus_min, tinicioT)
            
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
            
            ### tg
            if self.entrada_tg_from_mp is not None:
                u_tg_t_array = self.entrada_tg_from_mp.iloc[i]
                u_tg = u_tg_t_array
                self.u_tg.iloc[i + 1, :] = u_tg_t_array
            # INTEGRACAO DOS SISTEMAS: SAIDA DE MP (VA_DOT) COMO ENTRADA DE TG (QA) - FLUXO ALVEOLAR
            elif VA_dot_mp is not None:
                u_tg = VA_dot_mp
                # u_tg = u_tg_t_array
                self.u_tg.iloc[i+1, :] = u_tg
            else:
                # u em t
                phi = 2 * m.pi * f * t
                u_tg_t_array = entrada_tg(phi=phi, Pfis=Pfis) # QA
                u_tg = u_tg_t_array
                self.u_tg.iloc[i+1, :] = u_tg_t_array

            x_tg_array = self.x_tg.iloc[i, 0:].to_numpy()
            x_tg = x_tg_array

            # constantes para RK2
            k1_tg_rk2 = derivada_tg(x_tg, u_tg, cts_tg)
            k2_tg_rk2 = derivada_tg(x_tg, u_tg, cts_tg)

            # atribuindo os valores em x
            x_tg_rk2 = x_tg + dt*(k1_tg_rk2 + k2_tg_rk2)/2
            self.x_tg.iloc[i+1, :] = pd.DataFrame(np.matrix(x_tg_rk2))

            # atribuindo os valores em y
            self.y_tg.iloc[i + 1, :] = saida_tg(x_tg_rk2, cts_tg)
            
            tciclo, T, Te, Ti, RR, Pmus_min, tinicioT \
                = tciclo_dt, T_dt, Te_dt, Ti_dt, RR_dt, Pmus_min_dt, tinicioT_dt