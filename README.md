# Modelo_MecPulmTrocGas

## normal - simulacao repouso parametros iniciais
### 1. repouso
    self.x_tg.iloc[0, 0] = 11.94
    self.x_tg.iloc[0, 1] = 0.36
    self.x_tg.iloc[0, 2] = 58.34

    self.x_tg.iloc[0, 3] = 0.68
    self.x_tg.iloc[0, 4] = 0.26

    self.x_tg.iloc[0, 5] = 198.75 
    self.x_tg.iloc[0, 6] = 101.48

    "Q_O2_Alb": ((0.2 / 1000) / 60),
    "Q_b": (5.6 / 60) / 1000
    "RR": 12,
    "Pmus_min": -5,

    resultados:
    - rr: 12
    - Q_b: 5.6
    - pmusmin: -5

    - Vcorrente: 0.5 L
    - VD: 140-180mL
    - QA: 0.36 L/s máx.
    - valores finais PcapO2: 95-99 mmHg; PcapCO2: 37.3-38.5 mmHg 

### 2. atividade
    self.x_tg.iloc[0, 0] = 11.98536
    self.x_tg.iloc[0, 1] = 0.366351
    self.x_tg.iloc[0, 2] = 58.446508

    self.x_tg.iloc[0, 3] = 0.7098
    self.x_tg.iloc[0, 4] = 0.275655

    self.x_tg.iloc[0, 5] = 208.18697 
    self.x_tg.iloc[0, 6] = 104.956376

    "Q_O2_Alb": ((2.88 / 1000) / 60), # aumento do consumo de O2
    "Q_b": (5.6 / 60) / 1000
    "RR": 12,
    "Pmus_min": -5,

    resultados limite 42
    - rr: 20 (iniciou em 40 e max em 134)
    - Q_b: 25.6
    - pmusmin: -14.629

    - Vcorrente: 1.5 L
    - VD: 140-240mL
    - QA: 1.57 (x4.5).
    - valores finais PcapO2: 45-63 mmHg; PcapCO2: 35-44 mmHg 

### 3. recuperacao
    self.x_tg.iloc[0, 0] = 7.410413
    self.x_tg.iloc[0, 1] = 0.483415
    self.x_tg.iloc[0, 2] = 59.951817

    self.x_tg.iloc[0, 3] = 1.093856
    self.x_tg.iloc[0, 4] = 0.817523

    self.x_tg.iloc[0, 5] =  276.714609
    self.x_tg.iloc[0, 6] = 310.085402

    "Q_O2_Alb": ((0.2 / 1000) / 60), # normalidade do consumo de O2
    "Q_b": (25.6 / 60) / 1000, # obter dos resultados
    "RR": 20, # obter dos resultados
    "Pmus_min": -14.629, # obter dos resultados

    resultados limite 42
    - rr: 13
    - Q_b: 8.1
    - pmusmin: -7.6

    - Vcorrente: 0.7 L
    - VD: 140-190mL
    - QA: 0.5.
    - valores finais PcapO2: 85-90 mmHg; PcapCO2: 41-42 mmHg 

##  DPOC - simulacao atividade dpoc alteracoes
    Integracao(resistencia_alveolar=40, fator_difusao=0.9)

### parametros iniciais
### 1. repouso
    self.x_tg.iloc[0, 0] = 12.339234
    self.x_tg.iloc[0, 1] = 0.362266
    self.x_tg.iloc[0, 2] = 58.836508

    self.x_tg.iloc[0, 3] = 0.712674 
    self.x_tg.iloc[0, 4] = 0.285165

    self.x_tg.iloc[0, 5] = 213.698278
    self.x_tg.iloc[0, 6] = 108.356058

    "Q_O2_Alb": ((0.2 / 1000) / 60),
    "Q_b": (5.6 / 60) / 1000
    "RR": 12,
    "Pmus_min": -5,

    resultados limite 42
    - rr: 12
    - Q_b: 5.6
    - pmusmin: -5

    - Vcorrente: 0.42 L
    - VD: 140-180mL
    - QA: 0.27.
    - valores finais PcapO2: 94-97 mmHg; PcapCO2: 38-39 mmHg 

### 2. atividade
    self.x_tg.iloc[0, 0] = 11.94
    self.x_tg.iloc[0, 1] = 0.37
    self.x_tg.iloc[0, 2] = 58.73

    self.x_tg.iloc[0, 3] = 0.68
    self.x_tg.iloc[0, 4] = 0.27

    self.x_tg.iloc[0, 5] = 205.49
    self.x_tg.iloc[0, 6] = 104.82

    "Q_O2_Alb": ((2.88 / 1000) / 60), # aumento do consumo de O2
    "Q_b": (5.6 / 60) / 1000
    "RR": 12,
    "Pmus_min": -5,

    resultados limite 42
    - rr: 20 (inicio 35 e max em 124)
    - Q_b: 25.6
    - pmusmin: -14.629

    - Vcorrente: 1 L
    - VD: 140-260mL
    - QA: 1 (aumentou x3.7).
    - valores finais PcapO2: 39-54 mmHg; PcapCO2: 32-41 mmHg 

### 3. recuperacao
    self.x_tg.iloc[0, 0] = 10.866279
    self.x_tg.iloc[0, 1] = 0.696741
    self.x_tg.iloc[0, 2] = 85.071578

    self.x_tg.iloc[0, 3] = 1.030086
    self.x_tg.iloc[0, 4] = 0.772208

    self.x_tg.iloc[0, 5] = 249.045561
    self.x_tg.iloc[0, 6] = 293.277007

    "Q_O2_Alb": ((0.2 / 1000) / 60), # normalidade do consumo de O2
    "Q_b": (25.6 / 60) / 1000, # obter dos resultados
    "RR": 20, # obter dos resultados
    "Pmus_min": -14.629, # obter dos resultados

    resultados limite 42
    - rr: 12
    - Q_b: 5.6
    - pmusmin: -5

    - Vcorrente: 0.42 L
    - VD: 140-180mL
    - QA: 0.27.
    - valores finais PcapO2: 88-91 mmHg; PcapCO2: 39-40 mmHg 

# Como executar o modelo integrado:
Alterar o arquivo input.json e executar main.py.
## input.json, escolhas possiveis:
- save_figures: TRUE/FALSE
- save_data: TRUE/FALSE
- modo_ventilacao: normal/dpoc
- modo_atividade: repouso/exercicio/recuperacao
- tempo_simulacao: 1-1000 [segundos]
# 
    {
        "save_figures": "FALSE",
        "save_data": "FALSE",
        "modo_ventilacao": "normal",
        "modo_atividade": "repouso",
        "tempo_simulacao": "100"
    }
