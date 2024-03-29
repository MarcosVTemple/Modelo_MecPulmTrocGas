import os
import numpy as np
import matplotlib.pyplot as plt


def plot_tg(t, x, y, u):
    plt.figure(1)
    plt.title("Gas Exchange - no. Mols - Alveolar Compartiment")
    plt.xlabel("Time (s)")
    plt.ylabel("no. Mols [mmol]")
    plt.plot(t, np.array(x["n_A_O2"]), color="r", label="n_A_O2")
    plt.plot(t, np.array(x["n_A_CO2"]), color="b", label="n_A_CO2")
    plt.plot(t, np.array(x["n_A_N2"]), color="g", label="n_A_N2")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/tg/figures/1_mols_alveolo_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}"
        ) 
    # plt.show()

    plt.figure(2)
    plt.title("Gas Exchange - no. Mols - Capillary Compartment")
    plt.xlabel("Time (s)")
    plt.ylabel("no. Mols [mmol]")
    plt.plot(t, np.array(x["n_cap_O2"]), color="r", label="n_cap_O2")
    plt.plot(t, np.array(x["n_cap_CO2"]), color="k", label="n_cap_CO2")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/tg/figures/2_mols_capilar_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}"
        )

    plt.figure(3)
    plt.title("Gas Exchange - no. Mols - Tissue Compartment")
    plt.xlabel("Time (s)")
    plt.ylabel("no. Mols [mmol]")
    plt.plot(t, np.array(x["n_t_O2"]), color="r", label="n_t_O2")
    plt.plot(t, np.array(x["n_t_CO2"]), color="k", label="n_t_CO2")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/tg/figures/3_mols_tecidual_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}"
        )

    plt.figure(4)
    plt.title("Gas Exchange - Alveolar Air Flow")
    plt.xlabel("Time (s)")
    plt.ylabel("Air Flow [L/s]")
    plt.plot(t, np.array(u["VA_dot"]), color="r", label="VA_dot")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/tg/figures/4_vazao_alveolo_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}"
        )

    plt.figure(5)
    plt.title("Gas Exchange - Partial Pressure - Alveolar Compartiment")
    plt.xlabel("Time (s)")
    plt.ylabel("Partial Pressure [mmHg]")
    plt.plot(t, np.array(y["P_A_O2"]), color="r", label="P_A_O2")
    plt.plot(t, np.array(y["P_A_CO2"]), color="b", label="P_A_CO2")
    plt.plot(t, np.array(y["P_A_N2"]), color="g", label="P_A_N2")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/tg/figures/5_pparcial_alveolo_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}"
        )

    plt.figure(6)
    plt.title("Gas Exchange - Partial Pressure - Capillary Compartment")
    plt.xlabel("Time (s)")
    plt.ylabel("Partial Pressure [mmHg]")
    plt.plot(t, np.array(y["P_cap_O2"]), color="r", label="P_cap_O2")
    plt.plot(t, np.array(y["P_cap_CO2"]), color="b", label="P_cap_CO2")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/tg/figures/6_pparcial_capilar_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}"
        )
        
    plt.figure(7)
    # plt.title("Gas Exchange - Partial Pressure - Capillary Compartment")
    plt.xlabel("Time (s)")
    plt.ylabel("Partial Pressure [mmHg]")
    plt.plot(t, np.array(y["P_cap_O2"]), color="r", label="P_cap_O2")
    plt.plot(t, np.array(y["P_cap_CO2"]), color="b", label="P_cap_CO2")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/tg/figures/6_pparcial_capilar_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}"
        )
    else:
        plt.show()
