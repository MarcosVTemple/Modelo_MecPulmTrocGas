import numpy as np
import math as m


def entrada_tg(phi, Pfis):
    QA = Pfis * m.sin(phi)
    u = QA
    return u
