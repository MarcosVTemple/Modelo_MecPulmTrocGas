cts_mp = {
    #### MECANICA PULMONAR ####
    "N": 500000,
    "dt": 0.0004,
    # COMPLIANCE l/cmH2O
    "Cl": 0.00127,
    "Ctr": 0.00238,
    "Ccw": 0.2445,
    "Cb": 0.0131,
    "CA": 0.2,
    # RESISTANCE cmH2O·s/l
    "Rtb": 0.3063,
    "Rlt": 0.3369,
    "Rml": 1.021,
    "RbA": 0.0817,
    # UNSTRESSED VOLUME L
    "Vul": 0.0344,
    "Vut": 0.00663,
    "Vub": 0.0187,
    "VuA": 1.263,
    # ADDITIONAL PARAMETERS
    "IEratio": 0.6,
    "RR": 12,   # breaths/min
    "Pmus_min": -5,  # cmH2O
    "Ppl_EE": -5,  # cmH2O
    "Ti": 1.875,  # [s]
    "Te": 3.125,  # [s]
    "T": 5,   # [s]
    "Pao": 0,  #At the beginning of inspiration, alveolar pressure equals Patm, i.e., zero pressure,  # cmH2O
    "Pvent": 0,
}
cts_tg = {
    # "N": 30000, funcionando
    "N": 60000,
    "dt": 0.0004,
    "R": 8.314,                     # Cte universal gases ideais [Pa.m3/mol.K]
    "Temp": 273 + 36.5,             # Temperatura corporal [K]
    # "VA_t": 2.2 / 1000,             # volume alveolar antes da inspiração 2.2 [L] - 0.0022 [m3]
    "VA_t": 1.263 / 1000,             # volume alveolar unstressed ursino
    "Patm": 100000,                 # 100000 [Pa] - 1 [atm] - 760 [mmHg]
    "Patm_pulmao": 100000,                 # 100000 [Pa] - (760 - 47 p vapor agua) [mmHg]
    "Pfis": 1.5,                    # Amplitude de Pw
    # "f_O2":  0.2094,                 # fração do gas na atm
    # "f_CO2": 0.0038,                # fração do gas na atm
    # "f_N2_H2O": 0.7868,                  # fração do gas na atm
    "f_O2": 0.1368,  # fração do gas no alveolo
    "f_CO2": 0.0526,  # fração do gas no alveolo
    "f_N2_H2O": 0.8105,  # fração do gas no alveolo
    "D_O2_Alb": 32.253e-10,         # 26 [ml/min.mmHg] - 0.00043 [L/s.mmHg] - 32.253e-10 [m³/s.Pa]
    # "D_O2": (D_O2_Alb) * ((Patm) / (R * T)) * 1000  # convertido em mmols
    "D_CO2_Alb": 22.502e-09,        # 180 [ml/min.mmHg] - 0.003 [L/s.mmHg] - 22.502e-09 [m³/s.Pa]
    # "D_CO2": D_CO2_Alb * ((Patm) / (R * T)) * 1000  # convertido em mmols
    # derivada capilar
    "sigma": 0.98,                  #  pulmonary shunts -> capilares
    "Vt": 37.35 / 1000,             # Volume tecidos musculares/nao musc/capilares tec
    "Vcap": 0.1 / 1000,             # m3
    # derivada tecidual
    "n_t_O2_fis": 208,              # número de mols do gás O2 nos tecidos (fisiológico) [mmol]
    "n_t_CO2_fis": 76,              # número de mols do gás CO2 nos tecidos (fisiológico) [mmol]
    "c_t_O2_fis": 19607,            # n_t_O2/Vt   [mmol/m3] ## VERIFICAR SE É 14.6 ml/100ml
    "c_t_CO2_fis": 4610.1,          # n_t_CO2/Vt [mmol/m3] ## VERIFICAR SE É 52.6 ml/100ml

    # DEFINIR VENTILACAO E PARAMS

    "modo_ventilacao": "normal",
    # "modo_ventilacao": "apneia",
    # Repouso
        "Q_O2_Alb": ((0.3 / 1000) / 60),        # proporção do consumo do gás O2 [m3/s] 200-300 ml/min
        #### "Q_O2": (Q_O2_Alb * (Patm / (R * T))) * 1000  # proporção do consumo do gás O2 [mmol/s]
        "Q_b": (5.6 / 60) / 1000,  # 5.6 L/min - 5.6/1000 m3
        "RR": 12,                                   # breaths/min eupneia (normal)
    # Aumentado
        # "Q_O2_Alb": ((2.88/1000)/60),       # AUMENTADO: proporção do consumo do gás O2 [m3/s] 2880 ml/min
        #### "Q_b": ((5.6 / 60) / 1000) * 60,          # AUMENTADO APNEIA #5.6 L/min - 5.6/1000 m3
        # "Q_b": (25.6/60)/1000,                      # AUMENTADO SENOIDAL 25.6 L/min - 5.6/1000 m3 (Corrida)
        # "RR": 20,                                   # breaths/min

    # (URSINO)
    ## environmental Conditions
    # "sigma": 0.9830,  #  pulmonary shunts -> capilares (URSINO)
    # "f_O2": 0.210379,                   # fração do gas na atm
    # "f_CO2": 0.000421,                  # fração do gas na atm
    # "K_ar": 1.2103,                     # Compressao
    # "Patm_mmHg": 760,                   # Pressão atmosférica - mmHg
    # "Pws_mmHg": 47,                     # Pressão ?? - mmHg
    # ## Dissociation Curves
    # "Csat_O2": 9,                       # mmol/l
    # "Csat_CO2": 86.11,                  # mmol/l
    # "h1": 0.3836,                       # cte
    # "h2": 1.819,                        # cte
    # "alfa1": 0.03198,                   # mmHg-1
    # "alfa2": 0.05591,                   # mmHg-1
    # "beta1": 0.008275,                  # mmHg-1
    # "beta2": 0.03255,                   # mmHg-1
    # "K1": 14.99,                        # mmHg
    # "K2": 194.4,                        # mmHg
    # ## Physiological status
    # "sh": 1.7,                          # shunt percentage - cte
    # "Hgb": 15,                          # 15 g/dl
    # ## Consumo e Producao
    # "M_O2": 250,        # ml/min
    # "M_CO2": 210,        # ml/min
    # "QR": 0.84,        # ml/min
}

cts_int = {
    "dt": 0.0004,
    "RR": 12,
    "T": 5,
    "IEratio": 0.6
}