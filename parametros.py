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
    "N": 60000,
    "dt": 0.0004,
    "R": 8.314,                     # Cte universal gases ideais [Pa.m3/mol.K]
    "Temp": 273 + 36.5,             # Temperatura corporal [K]
    "VA_t": 1.263 / 1000,             # volume alveolar unstressed ursino
    "Patm": 101325,                 # 100000 [Pa] - 1 [atm] - 760 [mmHg]
    "f_O2":  0.2094,                 # fração do gas na atm
    "f_CO2": 0.0038,                # fração do gas na atm
    "f_N2_H2O": 0.7868,                  # fração do gas na atm
    "D_O2_Alb": 32.253e-10,         # 26 [ml/min.mmHg] - 0.00043 [L/s.mmHg] - 32.253e-10 [m³/s.Pa]
    "D_O2": 2.555227969833428e-05,
    "D_CO2_Alb": 22.502e-09,        # 180 [ml/min.mmHg] - 0.003 [L/s.mmHg] - 22.502e-09 [m³/s.Pa]
    "D_CO2": 8.78457682709007e-07,
    # derivada capilar
    "sigma": 0.98,                  #  pulmonary shunts -> capilares
    "Vt": 37.35 / 1000,             # Volume tecidos musculares/nao musc/capilares tec
    "Vcap": 0.1 / 1000,             # m3
    # derivada tecidual
    "n_t_O2_fis": 208,              # número de mols do gás O2 nos tecidos (fisiológico) [mmol]
    "n_t_CO2_fis": 76,              # número de mols do gás CO2 nos tecidos (fisiológico) [mmol]
    "c_t_O2_fis": 19607,            # n_t_O2/Vt   [mmol/m3] 
    "c_t_CO2_fis": 4610.1,          # n_t_CO2/Vt [mmol/m3] 

    # DEFINIR VENTILACAO E PARAMS
    # "modo_ventilacao": "normal", #  "apneia",
    # Repouso
        # "Q_O2_Alb": ((0.2 / 1000) / 60),        # proporção do consumo do gás O2 [m3/s] 200-300 ml/min
        # "Q_b": (5.6 / 60) / 1000,               # 5.6 L/min - 5.6/1000 m3
    # Aumentado
        # "Q_O2_Alb": ((2.88/1000)/60),         # AUMENTADO: proporção do consumo do gás O2 [m3/s] 2880 ml/min
        # "Q_b": (5.6 / 60) / 1000,             # inicialmente 5.6 L/min - 5.6/1000 m3
    # Recuperacao
        # "Q_O2_Alb": ((0.2/1000)/60),
        # "Q_b": (25.6 / 60) / 1000,
        
    # novo
    "repouso": {
        "Q_O2_Alb": ((0.2 / 1000) / 60),
        "Q_b": (5.6 / 60) / 1000,
        "normal": {
            "nmols_inicial_A_O2": 11.94,
            "nmols_inicial_A_CO2": 0.36,
            "nmols_inicial_A_N2": 58.34,
            "nmols_inicial_cap_O2": 0.68,
            "nmols_inicial_cap_CO2": 0.26,
            "nmols_inicial_t_O2": 198.75 ,
            "nmols_inicial_t_CO2": 101.48,
        },
        "dpoc": {
            "nmols_inicial_A_O2": 12.339234,
            "nmols_inicial_A_CO2": 0.362266,
            "nmols_inicial_A_N2": 58.836508,
            "nmols_inicial_cap_O2": 0.712674 ,
            "nmols_inicial_cap_CO2": 0.285165,
            "nmols_inicial_t_O2": 213.698278,
            "nmols_inicial_t_CO2": 108.356058,            
        }
    },    
    "exercicio": {
        "Q_O2_Alb": ((2.88 / 1000) / 60),
        "Q_b": (5.6 / 60) / 1000,
        "normal": {
            "nmols_inicial_A_O2": 11.98536,
            "nmols_inicial_A_CO2": 0.366351,
            "nmols_inicial_A_N2": 58.446508,
            "nmols_inicial_cap_O2": 0.7098,
            "nmols_inicial_cap_CO2": 0.275655,
            "nmols_inicial_t_O2": 208.18697,
            "nmols_inicial_t_CO2": 104.956376,
        },
        "dpoc": {
            "nmols_inicial_A_O2": 12.339234,
            "nmols_inicial_A_CO2": 0.362266,
            "nmols_inicial_A_N2": 58.836508,
            "nmols_inicial_cap_O2": 0.712674 ,
            "nmols_inicial_cap_CO2": 0.285165,
            "nmols_inicial_t_O2": 213.698278,
            "nmols_inicial_t_CO2": 108.356058, 
        }
    },    
    "recuperacao": {
        "Q_O2_Alb": ((0.2/1000)/60),
        "Q_b": (25.6 / 60) / 1000,  # obtido dos resultados do exercicio
        "normal": {
            "nmols_inicial_A_O2": 10.960723,
            "nmols_inicial_A_CO2": 0.590381,
            "nmols_inicial_A_N2": 76.68942,
            "nmols_inicial_cap_O2": 1.119221,
            "nmols_inicial_cap_CO2": 0.798921,
            "nmols_inicial_t_O2": 267.249815,
            "nmols_inicial_t_CO2": 303.791726,
        },
        "dpoc": {
            "nmols_inicial_A_O2": 7.18276,
            "nmols_inicial_A_CO2": 0.55175,
            "nmols_inicial_A_N2": 65.497885,
            "nmols_inicial_cap_O2": 0.952438,
            "nmols_inicial_cap_CO2": 0.784887,
            "nmols_inicial_t_O2": 246.832904,
            "nmols_inicial_t_CO2": 297.079979,
        }
    },    
    
}

cts_int = {
    # variaveis por simulacao
    # "RR": 12,
    # "Pmus_min": -5, # -5,-14.629
    
    "repouso": {
        "RR": 12,
        "Pmus_min": -5,
    },    
    "exercicio": {
        "RR": 12,
        "Pmus_min": -5,
    },    
    "recuperacao": {
        "RR": 20, # obtido dos resultados do exercicio
        "Pmus_min": -14.629, # obtido dos resultados do exercicio
    },
    
    # fixos
    "incremento_rr": 1,
    "dt": 0.0004,
    "T": 5,
    "IEratio": 0.6,
    "Q_b_repouso": (5.6 / 60) / 1000,
    "Q_b_corrida": (25.6 / 60) / 1000,
    "RR_repouso": 12,
    "RR_corrida": 20,
    "D_O2_repouso": 2.555227969833428e-05,
    "D_CO2_repouso": 8.78457682709007e-07,
    "D_O2_corrida": 2.555227969833428e-05*10, # fig 6 - hammond e hempleman (* 2.4)
    "D_CO2_corrida": 8.78457682709007e-07*10, #
    
}

# alterar entrada de ar com as proporcoes do ar atm

# testes (condições iniciais: RR, Q_O2_Alb, nmols inicial)
## 1 - condições iniciais: RR e nmols em repouso com consumo em repouso (verificar o regime permanente) - simular comportamento das pressões parciais ao repouso
## 2 - condições iniciais: RR e nmols em repouso em rp com consumo aumentado (verificar o regime transiente) - simular adequação das pressões parciais ao consumo aumentado (ex.: exercício repentino) 
## 3 - condições iniciais: RR e nmols aumentado com consumo aumentado (verificar o regime permanente) - simular comportamento das pressões parciais ao consumo aumentado (ex.: exercício contínuo) 
## 4 - condições iniciais: RR e nmols aumentado com consumo em repouso (verificar o regime transiente) - simular adequação das pressões parciais ao repouso (ex.: exercício interrompido) 

# Pressões parciais, volumes, fluxos,

# resultados