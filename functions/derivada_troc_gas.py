import os
import numpy as np


def derivada_tg(x, u, cts_tg):
    modo_atividade = os.getenv("modo_atividade")
    n_A_O2, n_A_CO2, n_A_N, n_cap_O2, n_cap_CO2, n_t_O2, n_t_CO2 = x

    R, T, Patm, f_O2, f_CO2, f_N, D_O2, D_CO2, Q_b, sigma, \
    Vt, Vcap, c_t_O2_fis, Q_O2 = get_constants(cts_tg, modo_atividade)


    nT = n_A_O2 + n_A_CO2 + n_A_N  # numero de mmols total no alveolo

    nT_t = ((-n_t_O2 - n_t_CO2) * (nT / n_A_N)) / (1 - (nT / n_A_N)) # numero de mmols total nos tecidos


    # derivada alveolar
    if u >= 0:
        dn_A_O2 = (D_O2 * Patm) * (-(n_A_O2 / nT) + (n_t_O2 / nT_t)) + ((Patm * f_O2) / (R * T)) * u
        dn_A_CO2 = (D_CO2 * Patm) * (-(n_A_CO2 / nT) + (n_t_CO2 / nT_t)) + ((Patm * f_CO2) / (R * T)) * u
        dn_A_N = 0 + ((Patm * f_N) / (R * T)) * u
        PA = Patm * (f_CO2 + f_O2 + f_N)
    else:
        PA_O2 = n_A_O2 * (Patm) / nT
        PA_CO2 = n_A_CO2 * (Patm) / nT
        PA_N = n_A_N * (Patm) / nT
        PA = PA_O2 + PA_CO2 + PA_N
        dn_A_O2 = (D_O2 * Patm) * (-(n_A_O2 / nT) + (n_t_O2 / nT_t)) + ((PA_O2) / (R * T)) * u
        dn_A_CO2 = (D_CO2 * Patm) * (-(n_A_CO2 / nT) + (n_t_CO2 / nT_t)) + ((PA_CO2) / (R * T)) * u
        dn_A_N = ((Patm * f_N) / (R * T)) * u

    # derivada capilar
    dn_cap_O2 = (D_O2 * Patm) * ((n_A_O2 / nT) - (n_t_O2 / nT_t)) + (Q_b * sigma) * (
                (n_t_O2 / Vt) - (n_cap_O2 / Vcap))
    dn_cap_CO2 = (D_CO2 * Patm) * ((n_A_CO2 / nT) - (n_t_CO2 / nT_t)) + (Q_b * sigma) * (
                 (n_t_CO2 / Vt) - (n_cap_CO2 / Vcap))

    # derivada tecidual
    K_O2 = Q_O2 / c_t_O2_fis
    K_CO2 = 0.85 * K_O2
    
    dn_t_O2 = Q_b * sigma * ((-n_t_O2 / Vt) + (n_cap_O2 / Vcap)) - K_O2 * (n_cap_O2 / Vcap)
    dn_t_CO2 = Q_b * sigma * ((-n_t_CO2 / Vt) + (n_cap_CO2 / Vcap)) + K_CO2 * (n_cap_O2 / Vcap)

    dx = np.array([dn_A_O2, dn_A_CO2, dn_A_N, dn_cap_O2, dn_cap_CO2, dn_t_O2, dn_t_CO2])
    return dx


def get_constants(cts_tg, modo_atividade):
    R = cts_tg["R"]
    T = cts_tg["Temp"]
    VA_t = cts_tg["VA_t"]
    Patm = cts_tg["Patm"]
    f_O2 = cts_tg["f_O2"]
    f_CO2 = cts_tg["f_CO2"]
    f_N = cts_tg["f_N2_H2O"]
    D_O2 = cts_tg["D_O2"]
    D_CO2 = cts_tg["D_CO2"]
    Q_b = cts_tg[modo_atividade]["Q_b"]
    sigma = cts_tg["sigma"]
    Vt = cts_tg["Vt"]
    Vcap = cts_tg["Vcap"]
    c_t_O2_fis = cts_tg["c_t_O2_fis"]
    Q_O2_Alb = cts_tg[modo_atividade]["Q_O2_Alb"]
    
    # calculado com base nos valores iniciais de n para os 3 compartimentos e derivada zero
    # D_O2 = 0.00010646783207639284 
    # D_O2 = D_O2 - D_O2 * 0.76
   
    # D_CO2 = 4.3922884135450315e-05 # (aumentar em 40%)
    # D_CO2 = D_CO2 - D_CO2 * 0.98
   
    Q_O2 = (Q_O2_Alb * (Patm / (R * T))) * 1000

    return R, T, Patm, f_O2, f_CO2, f_N, D_O2, D_CO2, Q_b, sigma, Vt, Vcap, \
           c_t_O2_fis, Q_O2
