from tqdm import tqdm
import pandas as pd
import numpy as np
import math as m
import time as t
import os

from parametros import cts_mp, cts_tg, cts_int
from functions.plot_integracao import plot_int
from functions.controle_mec_pulm import controle_mp, get_params_controle_calc

from functions.entrada_troc_gas import entrada_tg
from functions.derivada_troc_gas import derivada_tg
from functions.saida_troc_gas import saida_tg
from functions.plot_troc_gas import plot_tg

from parametros import cts_mp
from functions.derivada_mec_pulm import derivada_mp
from functions.entrada_mec_pulm import entrada_mp
from functions.saida_mec_pulm import saida_mp
from functions.plot_mec_pulm import plot_mp

from decorators.timefunc import timefunc

dt = cts_int["dt"]
T = cts_int["T"]
IEratio = cts_int["IEratio"]

Cl = cts_mp["Cl"]
Ctr = cts_mp["Ctr"]
Ccw = cts_mp["Ccw"]
Cb = cts_mp["Cb"]
CA = cts_mp["CA"]

Vul = cts_mp["Vul"]
Vut = cts_mp["Vut"]
Vub = cts_mp["Vub"]
VuA = cts_mp["VuA"]

Pmus_min = cts_mp["Pmus_min"]
Pao = cts_mp["Pao"]
# Pvent = cts_mp["Pvent"]
Pvent = None



class Integracao:
    def __init__(self, **kwargs):
        self.modo_ventilacao = os.getenv("modo_ventilacao")
        self.modo_atividade = os.getenv("modo_atividade")
        
        self.resistencia_alveolar = None
        self.fator_difusao = None
        
        if kwargs.get("resistencia_alveolar", "") != "":
            self.resistencia_alveolar = kwargs.get("resistencia_alveolar", "")
        if kwargs.get("fator_difusao", "") != "":
            self.fator_difusao = kwargs.get("fator_difusao", "")
        
        tempo_simulacao = os.getenv("tempo_simulacao", default=None)
        if tempo_simulacao:
            cts_int["N"] = int(int(tempo_simulacao)/cts_int["dt"])

        # mp
        Pl = np.zeros(cts_int["N"], dtype=float)
        Ptr = np.zeros(cts_int["N"], dtype=float)
        Pb = np.zeros(cts_int["N"], dtype=float)
        PA = np.zeros(cts_int["N"], dtype=float)
        Ppl = np.zeros(cts_int["N"], dtype=float)
        vetor_zero = np.zeros(cts_int["N"], dtype=float)
            
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
        n_A_O2 = np.zeros(cts_int["N"], dtype=float)
        n_A_CO2 = np.zeros(cts_int["N"], dtype=float)
        n_A_N2 = np.zeros(cts_int["N"], dtype=float)
        n_cap_O2 = np.zeros(cts_int["N"], dtype=float)
        n_cap_CO2 = np.zeros(cts_int["N"], dtype=float)
        n_cap_N2 = np.zeros(cts_int["N"], dtype=float)
        n_t_O2 = np.zeros(cts_int["N"], dtype=float)
        n_t_CO2 = np.zeros(cts_int["N"], dtype=float)
        n_t_N2 = np.zeros(cts_int["N"], dtype=float)
        P_A_O2 = np.zeros(cts_int["N"], dtype=float)
        P_A_CO2 = np.zeros(cts_int["N"], dtype=float)
        P_A_N2 = np.zeros(cts_int["N"], dtype=float)
        P_cap_O2 = np.zeros(cts_int["N"], dtype=float)
        P_cap_CO2 = np.zeros(cts_int["N"], dtype=float)
        P_cap_N2 = np.zeros(cts_int["N"], dtype=float)
        VA_dot = np.zeros(cts_int["N"], dtype=float)

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
        self.y_int = pd.DataFrame(
            {
                'RR': np.zeros(cts_int["N"], dtype=float),
                'Pmus_min': np.zeros(cts_int["N"], dtype=float),
                'Q_b': np.zeros(cts_int["N"], dtype=float),
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
        self.x_tg.iloc[0, 0] = cts_tg[self.modo_atividade][self.modo_ventilacao]["nmols_inicial_A_O2"]
        self.x_tg.iloc[0, 1] = cts_tg[self.modo_atividade][self.modo_ventilacao]["nmols_inicial_A_CO2"]
        self.x_tg.iloc[0, 2] = cts_tg[self.modo_atividade][self.modo_ventilacao]["nmols_inicial_A_N2"]

        self.x_tg.iloc[0, 3] = cts_tg[self.modo_atividade][self.modo_ventilacao]["nmols_inicial_cap_O2"]
        self.x_tg.iloc[0, 4] = cts_tg[self.modo_atividade][self.modo_ventilacao]["nmols_inicial_cap_CO2"]

        self.x_tg.iloc[0, 5] = cts_tg[self.modo_atividade][self.modo_ventilacao]["nmols_inicial_t_O2"]
        self.x_tg.iloc[0, 6] = cts_tg[self.modo_atividade][self.modo_ventilacao]["nmols_inicial_t_CO2"]
        
        
        
    def plot_integracao(self):
        plot_int(self.t, self.x_tg, self.y_tg, self.u_tg, self.x_mp, self.y_mp, self.u_mp, self.y_int)
        
    @timefunc
    def run_integracao(self):
        self.inicializa_var_estado()
        self.rungekutta4()
        
        result_folder = "int"
        if os.getenv("modo_ventilacao", default="") == 'dpoc':
            result_folder = "dpoc"
        
        # mp
        if os.getenv("save_data", default="") == 'TRUE':
            timestamp = str(int(round(t.time() * 1000)))
            self.x_mp.to_csv(f"temp/{result_folder}/data/mecanica_pulmonar_variaveis_estado_dt_{dt}_{cts_int['N']}_{timestamp}.csv", sep=";", index=False)
            self.u_mp.to_csv(f"temp/{result_folder}/data/mecanica_pulmonar_entradas_dt_{dt}_{cts_int['N']}_{timestamp}.csv", sep=";", index=False)
            self.y_mp.to_csv(f"temp/{result_folder}/data/mecanica_pulmonar_saidas_dt_{dt}_{cts_int['N']}_{timestamp}.csv", sep=";", index=False)
        
        # tg
        if os.getenv("save_data", default="") == 'TRUE':
            timestamp = str(int(round(t.time() * 1000)))
            self.x_tg.to_csv(
                f"temp/{result_folder}/data/troca_gases_variaveis_estado_dt_{dt}_{cts_tg['modo_ventilacao']}_{timestamp}.csv",
                sep=";",
                index=False
            )
            self.y_tg.to_csv(
                f"temp/{result_folder}/data/troca_gases_saidas_dt_{dt}_{cts_tg['modo_ventilacao']}_{timestamp}.csv",
                sep=";",
                index=False
            )
        print(f"Valores finais de nmols:\n{self.x_tg.tail(1)}")
        
            
    def rungekutta4(self):
        RR = cts_int[self.modo_atividade]["RR"]
        Pmus_min = cts_int[self.modo_atividade]["Pmus_min"]
        tinicioT = 0
        tciclo_anterior = 0
        P_cap_O2 = self.y_tg.loc[0, "P_cap_O2"]
        P_cap_CO2 = self.y_tg.loc[0, "P_cap_CO2"]
        
        Rtb, Rlt, Rml, RbA = cts_mp["Rtb"], cts_mp["Rlt"], cts_mp["Rml"], cts_mp["RbA"]
        
        if self.resistencia_alveolar:
            RbA *= self.resistencia_alveolar
            
        if self.fator_difusao:
            cts_tg['D_O2'] = cts_tg['D_O2']*self.fator_difusao
            cts_tg['D_CO2'] = cts_tg['D_CO2']*self.fator_difusao
        
        tciclo, T, Te, Ti, RR, Pmus_min, tinicioT \
                = controle_mp(0, RR, IEratio, dt, P_cap_O2, P_cap_CO2, Pmus_min, tinicioT, tciclo_anterior)
        
        
        for i in tqdm(range(cts_int["N"]-1)):
            ### MECANICA PULMONAR
            
            # u em t
            t = self.t[i]
            
            u_t_array, Pmus \
                = entrada_mp(Pmus_min, Pao, tciclo, T, Te, Ti, Pvent)
                
            self.u_mp.loc[i, 'dPmus'] = u_t_array[0]
            self.u_mp.loc[i, 'Pao_Pvent'] = u_t_array[1]
            self.u_mp.loc[i, 'Pmus'] = Pmus
            u_t = np.matrix(u_t_array).transpose()

            # u em t+dt
            t_dt = t + dt
            
            tciclo_dt, T_dt, Te_dt, Ti_dt, RR_dt, Pmus_min_dt, tinicioT_dt \
                = controle_mp(t_dt, RR, IEratio, dt, P_cap_O2, P_cap_CO2, Pmus_min, tinicioT, tciclo)
            
            u_dt_array, Pmus_dt \
                = entrada_mp(Pmus_min_dt, Pao, tciclo_dt, T_dt, Te_dt, Ti_dt, Pvent)
            u_dt = np.matrix(u_dt_array).transpose()

            # x em t
            x_array = self.x_mp.iloc[i, 0:].to_numpy()
            x = np.matrix(x_array).transpose()

            # constantes para RK2
            k1_rk2 = derivada_mp(x, u_t, Cl, Ctr, Ccw, Cb, CA, Rtb, Rlt, Rml, RbA)
            k2_rk2 = derivada_mp(x + k1_rk2*dt, u_dt, Cl, Ctr, Ccw, Cb, CA, Rtb, Rlt, Rml, RbA)

            # valores em x
            x_rk2 = x + dt*(k1_rk2+k2_rk2)/2
            self.x_mp.iloc[i+1, :] = pd.DataFrame(x_rk2.transpose())

            # valores em y
            self.y_mp.iloc[i + 1, :] = saida_mp(x_rk2, u_t, Cl, Ctr, Cb, CA, Rtb, Rlt, Rml, RbA, Vul, Vut, Vub, VuA)
            VA_dot_mp = self.y_mp.iloc[i + 1, 1]
            
            
            ### TROCA DE GASES
            
            # INTEGRACAO DOS SISTEMAS: SAIDA DE MP (VA_DOT) COMO ENTRADA DE TG (QA) - FLUXO ALVEOLAR
            u_tg = VA_dot_mp
            self.u_tg.iloc[i+1, :] = u_tg

            x_tg_array = self.x_tg.iloc[i, 0:].to_numpy()
            x_tg = x_tg_array

            # constantes para RK2
            k1_tg_rk2 = derivada_tg(x_tg, u_tg, cts_tg)
            k2_tg_rk2 = derivada_tg(x_tg, u_tg, cts_tg)

            # valores em x
            x_tg_rk2 = x_tg + dt*(k1_tg_rk2 + k2_tg_rk2)/2
            self.x_tg.iloc[i+1, :] = pd.DataFrame(np.matrix(x_tg_rk2))

            # valores em y
            self.y_tg.iloc[i + 1, :] = saida_tg(x_tg_rk2, cts_tg)
            
            ### CONTROLE
            Q_b = cts_tg[self.modo_atividade]["Q_b"]*1000*60
            self.y_int.iloc[i + 1, :] = np.array([RR_dt, Pmus_min_dt, Q_b])
            tciclo_anterior = tciclo
            
            tciclo, T, Te, Ti, RR, Pmus_min, tinicioT \
                = tciclo_dt, T_dt, Te_dt, Ti_dt, RR_dt, Pmus_min_dt, tinicioT_dt
            
            P_cap_O2 = self.y_tg.loc[i+1, "P_cap_O2"]
            P_cap_CO2 = self.y_tg.loc[i+1, "P_cap_CO2"]