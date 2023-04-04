from typing import Tuple

def controle_mp(t: float, RR: float, IEratio: float, dt: float, P_cap_O2: float, P_cap_CO2: float, Pmus_min: float, tinicioT: float) -> Tuple[float, float, float, float, float, float]:
    """
    Calcula parametros necessarios para a entrada

    :param t: instante no vetor de tempo [s]
    :param RR: frequencia respiratoria [breaths/min]
    :param IEratio: razãao entre o tempo de inspiracao e expiracao
    :return: tciclo, T, Te, Ti
    """
    T = 60 / RR
    Te = (60 / RR) / (1 + IEratio)
    Ti = T - Te

    # tciclo = t % T
    
    tciclo = (t - tinicioT) % T
    
    tciclo_anterior = (t - dt) % T
    inicio_do_ciclo_boolean = tciclo < tciclo_anterior
    
    a0  = 56.83163265
    a1  = -7.50340136
    a2  = 0.19557823
    if inicio_do_ciclo_boolean and t > 0:
        """
        Calcular tinicioT
        
        """
        tinicioT = tinicioT + T
    
    
        # if P_cap_CO2 < 40:
        #     if RR >= 12: 
        #         RR -= 0.05
        #         Pmus_min = a0 + a1*RR + a2*(RR**2)
        # else:
        #     if RR <= 20: 
        #         RR += 0.05
        #         Pmus_min = a0 + a1*RR + a2*(RR**2)

        print(f"Pressoes O2 e CO2: {P_cap_O2}, {P_cap_CO2}")
        print(f"P_cap_CO2 > 37: {P_cap_CO2 > 37}")
        print(f"Novo Pmus_min: {Pmus_min}")
        print(f"Nova frequencia: {RR}")
        print(f"tinicioT: {tinicioT}")
        print(f"T: {T}")
        print(f"Ti: {Ti}")
        print(f"Te: {Te}")
        
        """
        Calcular novos T, Ti, Te
        
        """
        # T = 60 / RR
        # Te = (60 / RR) / (1 + IEratio)
        # Ti = T - Te
        
    
    return (tciclo, T, Te, Ti, RR, Pmus_min, tinicioT)

"""
Intervalo de valores
RR (breaths/min): 12 normal, 20 maximo, 10 minimo (visto em reynalds, 1973)

Alteracoes
RR and the amplitude of the respiratory muscle pressure generator, Pmus,min 

Polynomial fit of dataset: Table1_Pmus,min, using function: a0+a1*x+a2*x^2
Y standard errors: Unknown
From x = 12 to x = 20
a0  = 56,831632653061 +/- 3,36395353135248
a1  = -7,50340136054419 +/- 0,433210537231291
a2  = 0,195578231292516 +/- 0,0135788430464888
--------------------------------------------------------------------------------------
Chi^2 = 0,0765306122448936
R^2 = 0,999900738505519
---------------------------------------------------------------------------------------
"""