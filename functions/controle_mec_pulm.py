from typing import Tuple
from parametros import cts_int, cts_tg

def controle_mp(t: float, RR: float, IEratio: float, dt: float, P_cap_O2: float, P_cap_CO2: float, Pmus_min: float, tinicioT: float, tciclo_anterior:float) -> Tuple[float, float, float, float, float, float]:
    """
    Calcula parametros necessarios para a entrada

    :param t: instante no vetor de tempo [s]
    :param RR: frequencia respiratoria [breaths/min]
    :param IEratio: razãao entre o tempo de inspiracao e expiracao
    :return: tciclo, T, Te, Ti
    """
    Q_b = None
    T = 60 / RR
    Te = (60 / RR) / (1 + IEratio)
    Ti = T - Te

    tciclo = (t - tinicioT) % T
    
    # tciclo_anterior = (t - dt) % T
    inicio_do_ciclo_boolean = tciclo < tciclo_anterior
    

    
    if inicio_do_ciclo_boolean and t > 0:
        tinicioT = tinicioT + T
    
        incremento_rr = 1
        if P_cap_CO2 > 40 or P_cap_O2 < 70:
             if RR <= 21.1:
                RR += incremento_rr
                Pmus_min, Q_b = get_params_controle_calc(RR)
        else:
            if RR >= 12.5: 
                RR -= incremento_rr
                Pmus_min, Q_b = get_params_controle_calc(RR)           
        
        Q_b_litro_minuto = cts_tg["Q_b"]*1000*60
        
        print(f"Pressoes O2 e CO2: {P_cap_O2}, {P_cap_CO2}")
        print(f"Novo Pmus_min: {Pmus_min}")
        print(f"Nova frequencia: {RR}")
        print(f"Novo Débito Cardíaco: {Q_b_litro_minuto}")
        print(f"Nova difusao O2: {cts_tg['D_O2']}")
        print(f"Nova difusao CO2: {cts_tg['D_CO2']}")
        print(f"tinicioT: {tinicioT}")
        print(f"tciclo: {tciclo}")
        print(f"tciclo_anterior: {tciclo_anterior}")
        print(f"T: {T}")
        print(f"Ti: {Ti}")
        print(f"Te: {Te}")
        print(f"t: {t}")
        print(f"dt: {dt}")
        
        T = 60 / RR
        Te = (60 / RR) / (1 + IEratio)
        Ti = T - Te
        
    
    return (tciclo, T, Te, Ti, RR, Pmus_min, tinicioT)

"""
Intervalo de valores
RR (breaths/min): 12 normal, 20 maximo, 10 minimo (visto em reynalds, 1973)

Alteracoes
RR and the amplitude of the respiratory muscle pressure generator, Pmus,min 
"""


def get_params_controle_calc(RR: float) -> Tuple[float,float]:
    """
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
    f(RR) = RR*Pmus_min
    
    Q_b_medio = ((Q_b_corrida - Q_b_repouso)*(f(RR_medio) - f(RR_repouso)) / (f(RR_corrida) - f(RR_repouso)) ) + Q_b_repouso
                
    """
    a0  = 56.83163265
    a1  = -7.50340136
    a2  = 0.19557823
    
    Pmus_min = a0 + a1*RR + a2*(RR**2)
    
    
    Q_b_repouso = cts_int["Q_b_repouso"]
    Q_b_corrida = cts_int["Q_b_corrida"]
    RR_repouso = cts_int["RR_repouso"]
    RR_corrida = cts_int["RR_corrida"]
    f_corrida = RR_corrida*Pmus_min
    f_repouso = RR_repouso*Pmus_min
    f_medio = RR*Pmus_min
    
    Q_b = ((Q_b_corrida - Q_b_repouso)*(f_medio - f_repouso) / (f_corrida - f_repouso) ) + Q_b_repouso
    cts_tg["Q_b"] = Q_b
       
    D_O2_repouso = cts_int["D_O2_repouso"]
    D_O2_corrida = cts_int["D_O2_corrida"]
    D_CO2_repouso = cts_int["D_CO2_repouso"]
    D_CO2_corrida = cts_int["D_CO2_corrida"]
       
    D_O2 = ((D_O2_corrida - D_O2_repouso)*(Q_b - Q_b_repouso) / (Q_b_corrida - Q_b_repouso) ) + D_O2_repouso
    cts_tg["D_O2"] = D_O2
    D_CO2 = ((D_CO2_corrida - D_CO2_repouso)*(Q_b - Q_b_repouso) / (Q_b_corrida - Q_b_repouso) ) + D_CO2_repouso
    cts_tg["D_CO2"] = D_CO2
    
    return Pmus_min, Q_b
