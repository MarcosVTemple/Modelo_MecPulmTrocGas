import os
import numpy as np
import matplotlib.pyplot as plt


def plot_mp(t, x, y, u):
    plt.figure(1)
    plt.title("Pulmonary Mechanics - Region Pressures")
    plt.xlabel("Time (s)")
    plt.ylabel("Pressure [cmH2O]")
    plt.plot(t, np.array(x["Pl"]), color="r", label="Pl")
    plt.plot(t, np.array(x["Ptr"]), color="b", label="Ptr")
    plt.plot(t, np.array(x["Pb"]), color="g", label="Pb")
    plt.plot(t, np.array(x["PA"]), color="k", label="PA")
    plt.plot(t, np.array(x["Ppl"]), color="y", label="Ppl")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/mp/figures/1_pressoes_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}"
        )

    plt.figure(2)
    plt.title("Pulmonary Mechanics - Air Flow")
    plt.xlabel("Time (s)")
    plt.ylabel("Air Flow [L/s]")
    plt.plot(t, np.array(y["V_dot"]), color="r", label="V_dot")
    plt.plot(t, np.array(y["VA_dot"]), color="b", label="VA_dot")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/mp/figures/2_fluxos_"
            f"{os.getenv('modo_ventilacao', 'normal')}_"
            f"{os.getenv('modo_atividade', 'repouso')}"
        )

    plt.figure(3)
    plt.title("Pulmonary Mechanics - Volumes")
    plt.xlabel("Time (s)")
    plt.ylabel("Volume [L]")
    plt.plot(t, np.array(y["VA"]), color="k", label="VA")
    plt.plot(t, np.array(y["V"]), label="V")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/mp/figures/3_volumes_"
            f"{os.getenv('modo_ventilacao', 'normal')}_"
            f"{os.getenv('modo_atividade', 'repouso')}"
        )

    plt.figure(4)
    plt.title("Pulmonary Mechanics - Volumes")
    plt.xlabel("Time (s)")
    plt.ylabel("Volume [L]")
    plt.plot(t, np.array(y["Vl"]), color="r", label="Vl")
    plt.plot(t, np.array(y["Vtr"]), color="b", label="Vtr")
    plt.plot(t, np.array(y["Vb"]), color="g", label="Vb")
    plt.plot(t, np.array(y["VD"]), color="y", label="VD")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/mp/figures/4_volumes_saida_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}"
        )

    plt.figure(5)
    plt.title("Pulmonary Mechanics - Input Calculated Pressures")
    plt.xlabel("Time (s)")
    plt.ylabel("Pressure [cmH2O]")
    plt.plot(t, np.array(u["Pmus"]), color="r", label="Pmus")
    plt.plot(t, np.array(u["dPmus"]), color="k", label="dPmus")
    # plt.plot(t, derivada_pmus, color="b", label="derivada_pmus")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/mp/figures/5_pressoes_entrada_"
            f"{os.getenv('modo_ventilacao','normal')}"
            f"_{os.getenv('modo_atividade','repouso')}"
        )

    plt.rcParams.update({'font.size': 15})
    fig, axs = plt.subplots(2)
    # fig.suptitle('Pulmonary Mechanics - Alveolar Pressure and Air Flow')
    axs[0].plot(t, np.array(x["PA"]), color="k", label="PA")
    axs[1].plot(t, np.array(y["V_dot"]), color="r", label="V_dot")
    axs[0].set(ylabel="Alveolar Pressure [cmH2O]")
    axs[1].set(xlabel="Time (s)",ylabel="Air Flow [L/s]")
    
    
    # plt.figure(6)
    # plt.title("Pulmonary Mechanics - Alveolar Pressure")
    # plt.xlabel("Time (s)")
    # plt.ylabel("Pressure [cmH2O]")
    # plt.plot(t, np.array(x["PA"]), color="k", label="PA")
    # plt.legend(loc="upper left")
    # if os.getenv("save_figures", default="") == 'TRUE':
    #     plt.savefig(
    #         f"temp/mp/figures/1_pressoes_"
    #         f"{os.getenv('modo_ventilacao','normal')}_"
    #         f"{os.getenv('modo_atividade','repouso')}"
    #     )

    # plt.figure(7)
    # plt.title("Pulmonary Mechanics - Air Flow")
    # plt.xlabel("Time (s)")
    # plt.ylabel("Air Flow [L/s]")
    # plt.plot(t, np.array(y["V_dot"]), color="r", label="V_dot")
    # plt.legend(loc="upper left")
    # if os.getenv("save_figures", default="") == 'TRUE':
    #     plt.savefig(
    #         f"temp/mp/figures/2_fluxos_"
    #         f"{os.getenv('modo_ventilacao', 'normal')}_"
    #         f"{os.getenv('modo_atividade', 'repouso')}"
    #     )
    plt.show()
