def controle_mp(t: float, RR: float, IEratio: float) -> (float, float, float, float):
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

    tciclo = t % T
    return tciclo, T, Te, Ti
