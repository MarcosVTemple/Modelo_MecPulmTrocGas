import numpy as np
import math as m

from funcoes.controle_mec_pulm import controle_mp


def entrada_mp(
    Pmus_min: float,
    Pao: float,
    tciclo, T, Te, Ti,
    Pvent: float = None,
) -> np.array:
    
    # tciclo, T, Te, Ti = controle_mp(t, RR, IEratio)
    tau = Te/5
    if tciclo <= Ti:  # inspiracao
        Pmus = (-Pmus_min / (Ti * Te)) * (tciclo**2) + ((Pmus_min * T) / (Ti * Te)) * tciclo
        dPmus = 2 * (-Pmus_min / (Ti * Te)) * tciclo + (Pmus_min * T / (Ti * Te))
    else:             # expiracao
        Pmus = (Pmus_min / (1 - m.exp(-Te / tau))) * (
            m.exp(-(tciclo - Ti) / tau) - m.exp(-Te / tau)
        )
        dPmus = (Pmus_min / (1 - m.exp(-Te / tau))) * ((-m.exp((Ti - tciclo) / tau)) / tau)

    u1 = dPmus
    u2 = Pvent if Pvent else Pao

    return np.array([u1, u2]), Pmus
