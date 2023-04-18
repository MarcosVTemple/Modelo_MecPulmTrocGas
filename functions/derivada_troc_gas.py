import numpy as np


def derivada_tg(x, u, cts_tg):
    n_A_O2, n_A_CO2, n_A_N, n_cap_O2, n_cap_CO2, n_t_O2, n_t_CO2 = x

    R, T, VA_t, Patm, f_O2, f_CO2, f_N, D_O2_Alb, D_O2, D_CO2_Alb, D_CO2, Q_b, Q_b, sigma, \
    Vt, Vcap, n_t_O2_fis, n_t_CO2_fis, c_t_O2_fis, c_t_CO2_fis, Q_O2_Alb, Q_O2, Q_O2, Q_CO2 = get_constants(cts_tg)


    nT = n_A_O2 + n_A_CO2 + n_A_N  # numero de mmols no ALVEOLO

    nT_cap = ((-n_cap_O2 - n_cap_CO2) * (nT / n_A_N)) / (1 - (nT / n_A_N))
    nT_t = ((-n_t_O2 - n_t_CO2) * (nT / n_A_N)) / (1 - (nT / n_A_N))

    if cts_tg["modo_ventilacao"] == "apneia":
        u = 0

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
    # dn_t_O2 = Q_b * sigma * ((-n_t_O2 / Vt) + (n_cap_O2 / Vcap)) - K_O2 * (n_t_O2 / Vt)
    # dn_t_CO2 = Q_b * sigma * ((-n_t_CO2 / Vt) + (n_cap_CO2 / Vcap)) + K_CO2 * (n_t_O2 / Vt)
    
    dn_t_O2 = Q_b * sigma * ((-n_t_O2 / Vt) + (n_cap_O2 / Vcap)) - K_O2 * (n_cap_O2 / Vcap)
    dn_t_CO2 = Q_b * sigma * ((-n_t_CO2 / Vt) + (n_cap_CO2 / Vcap)) + K_CO2 * (n_cap_O2 / Vcap)

    dx = np.array([dn_A_O2, dn_A_CO2, dn_A_N, dn_cap_O2, dn_cap_CO2, dn_t_O2, dn_t_CO2])
    return dx


def get_constants(cts_tg):
    R = cts_tg["R"]
    T = cts_tg["Temp"]
    VA_t = cts_tg["VA_t"]
    Patm = cts_tg["Patm"]
    f_O2 = cts_tg["f_O2"]
    f_CO2 = cts_tg["f_CO2"]
    f_N = cts_tg["f_N2_H2O"]
    D_O2_Alb = cts_tg["D_O2_Alb"]
    D_O2 = D_O2_Alb * (Patm / (R * T)) * 1000  # mmols
    D_CO2_Alb = cts_tg["D_CO2_Alb"]
    D_CO2 = D_CO2_Alb * (Patm / (R * T)) * 1000  # mmol
    Q_b = cts_tg["Q_b"]
    sigma = cts_tg["sigma"]
    Vt = cts_tg["Vt"]
    Vcap = cts_tg["Vcap"]
    n_t_O2_fis = cts_tg["n_t_O2_fis"]
    n_t_CO2_fis = cts_tg["n_t_CO2_fis"]
    c_t_O2_fis = cts_tg["c_t_O2_fis"]
    c_t_CO2_fis = cts_tg["c_t_CO2_fis"]
    Q_O2_Alb = cts_tg["Q_O2_Alb"]
    Q_O2 = (Q_O2_Alb * (Patm / (R * T))) * 1000  # mmol/s
    Q_CO2 = Q_O2 * 0.85  # mmol/s

    D_O2 = D_O2_Alb * ((Patm) / (R * T)) * 1000
    D_CO2 = D_CO2_Alb * ((Patm) / (R * T)) * 1000
    # calculado com base nos valores iniciais de n para os 3 compartimentos e derivada zero
    D_O2 = 0.00010646783207639284
    D_CO2 = 4.3922884135450315e-05
    Q_O2 = (Q_O2_Alb * (Patm / (R * T))) * 1000

    return R, T, VA_t, Patm, f_O2, f_CO2, f_N, D_O2_Alb, D_O2, D_CO2_Alb, D_CO2, Q_b, Q_b, sigma, Vt, Vcap, \
           n_t_O2_fis, n_t_CO2_fis, c_t_O2_fis, c_t_CO2_fis, Q_O2_Alb, Q_O2, Q_O2, Q_CO2
