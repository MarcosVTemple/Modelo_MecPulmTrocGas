import numpy as np


def saida_tg(x, cts_tg):
    PA_to_mmHg = 0.00750062
    n_A_T = sum(x[:3])

    n_A_O2, n_A_CO2, n_A_N2 = x[:3]
    P_O2 = ((n_A_O2 * cts_tg["Patm"]) / (n_A_T)) * PA_to_mmHg
    P_CO2 = ((n_A_CO2 * cts_tg["Patm"]) / (n_A_T)) * PA_to_mmHg
    P_N2 = ((n_A_N2 * cts_tg["Patm"]) / (n_A_T)) * PA_to_mmHg
    PA = np.array([P_O2, P_CO2, P_N2])

    n_cap_O2, n_cap_CO2 = x[3:5]
    n_cap_T = (n_A_T * (-n_cap_O2 - n_cap_CO2)) / (n_A_N2 - n_A_T) # 3.8862373954747875
    Pcap_O2 = cts_tg["Patm"] * (n_cap_O2/n_cap_T) * PA_to_mmHg
    Pcap_CO2 = cts_tg["Patm"] * (n_cap_CO2/n_cap_T) * PA_to_mmHg
    Pcap = np.array([Pcap_O2, Pcap_CO2])

    return np.append(PA, Pcap)
