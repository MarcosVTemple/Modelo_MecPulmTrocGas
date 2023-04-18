import os
import numpy as np
import matplotlib.pyplot as plt


def plot_int(t, x_tg, y_tg, u_tg, x_mp, y_mp, u_mp, y_int):
    ### mp 
    plt.figure(1)
    plt.title("Mecânica Pulmonar - Pressões")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Pressão [cmH2O]")
    plt.plot(t, np.array(x_mp["Pl"]), color="r", label="Pl")
    plt.plot(t, np.array(x_mp["Ptr"]), color="b", label="Ptr")
    plt.plot(t, np.array(x_mp["Pb"]), color="g", label="Pb")
    plt.plot(t, np.array(x_mp["PA"]), color="k", label="PA")
    plt.plot(t, np.array(x_mp["Ppl"]), color="y", label="Ppl")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/mp/figures/1_pressoes_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}"
        )

    plt.figure(2)
    plt.title("Mecânica Pulmonar - Fluxos")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Fluxo [L/s]")
    plt.plot(t, np.array(y_mp["V_dot"]), color="r", label="V_dot")
    plt.plot(t, np.array(y_mp["VA_dot"]), color="b", label="VA_dot")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/mp/figures/2_fluxos_"
            f"{os.getenv('modo_ventilacao', 'normal')}_"
            f"{os.getenv('modo_atividade', 'repouso')}"
        )

    plt.figure(3)
    plt.title("Mecânica Pulmonar - Volumes")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Volume [L]")
    plt.plot(t, np.array(y_mp["VA"]), color="k", label="VA")
    plt.plot(t, np.array(y_mp["V"]), label="V")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/mp/figures/3_volumes_"
            f"{os.getenv('modo_ventilacao', 'normal')}_"
            f"{os.getenv('modo_atividade', 'repouso')}"
        )

    plt.figure(4)
    plt.title("Mecânica Pulmonar - Volumes")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Volume [L]")
    plt.plot(t, np.array(y_mp["Vl"]), color="r", label="Vl")
    plt.plot(t, np.array(y_mp["Vtr"]), color="b", label="Vtr")
    plt.plot(t, np.array(y_mp["Vb"]), color="g", label="Vb")
    plt.plot(t, np.array(y_mp["VD"]), color="y", label="VD")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/mp/figures/4_volumes_saida_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}"
        )

    plt.figure(5)
    plt.title("Mecânica Pulmonar - Pressões de entrada")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Pressão [cmH2O]")
    plt.plot(t, np.array(u_mp["Pmus"]), color="r", label="Pmus")
    plt.plot(t, np.array(u_mp["dPmus"]), color="k", label="dPmus")
    # plt.plot(t, derivada_pmus, color="b", label="derivada_pmus")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/mp/figures/5_pressoes_entrada_"
            f"{os.getenv('modo_ventilacao','normal')}"
            f"_{os.getenv('modo_atividade','repouso')}"
        )
    # plt.show()

    
    ### tg
    plt.figure(6)
    plt.title("Troca de Gases - nº de Mols dos Gases no Compartimento Alveolar")
    plt.xlabel("Tempo [s]")
    plt.ylabel("nº de Mols [mmol]")
    plt.plot(t, np.array(x_tg["n_A_O2"]), color="r", label="n_A_O2")
    plt.plot(t, np.array(x_tg["n_A_CO2"]), color="b", label="n_A_CO2")
    plt.plot(t, np.array(x_tg["n_A_N2"]), color="g", label="n_A_N2")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/tg/figures/1_mols_alveolo_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}"
        ) 
    # plt.show()

    plt.figure(7)
    plt.title("Troca de Gases - nº de Mols dos Gases no Compartimento Capilar")
    plt.xlabel("Tempo [s]")
    plt.ylabel("nº de Mols [mmol]")
    plt.plot(t, np.array(x_tg["n_cap_O2"]), color="r", label="n_cap_O2")
    plt.plot(t, np.array(x_tg["n_cap_CO2"]), color="k", label="n_cap_CO2")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/tg/figures/2_mols_capilar_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}"
        )

    plt.figure(8)
    plt.title("Troca de Gases - nº de Mols dos Gases no Compartimento Tecidual")
    plt.xlabel("Tempo [s]")
    plt.ylabel("nº de Mols [mmol]")
    plt.plot(t, np.array(x_tg["n_t_O2"]), color="r", label="n_t_O2")
    plt.plot(t, np.array(x_tg["n_t_CO2"]), color="k", label="n_t_CO2")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/tg/figures/3_mols_tecidual_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}"
        )

    plt.figure(9)
    plt.title("Troca de Gases - Vazão Alveolar")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Fluxo [L/s]")
    plt.plot(t, np.array(u_tg["VA_dot"]), color="r", label="VA_dot")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/tg/figures/4_vazao_alveolo_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}"
        )

    plt.figure(10)
    plt.title("Troca de Gases - Pressões Parciais dos Gases no Compartimento Alveolar")
    plt.xlabel("Tempo [s]")
    plt.ylabel("P parcial [mmHg]")
    plt.plot(t, np.array(y_tg["P_A_O2"]), color="r", label="P_A_O2")
    plt.plot(t, np.array(y_tg["P_A_CO2"]), color="b", label="P_A_CO2")
    plt.plot(t, np.array(y_tg["P_A_N2"]), color="g", label="P_A_N2")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/tg/figures/5_pparcial_alveolo_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}"
        )

    plt.figure(11)
    plt.title("Troca de Gases - Pressões Parciais dos Gases no Compartimento Capilar")
    plt.xlabel("Tempo [s]")
    plt.ylabel("P parcial [mmHg]")
    plt.plot(t, np.array(y_tg["P_cap_O2"]), color="r", label="P_cap_O2")
    plt.plot(t, np.array(y_tg["P_cap_CO2"]), color="b", label="P_cap_CO2")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/tg/figures/6_pparcial_capilar_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}"
        )
    
        
    plt.figure(12)
    plt.title("Controle - Variação da Frequência Respiratória (RR)")
    plt.xlabel("Tempo [s]")
    plt.ylabel("RR [inc/min]")
    plt.plot(t, np.array(y_int["RR"]), color="r", label="RR")
    plt.legend(loc="upper left")
        
    plt.figure(13)
    plt.title("Controle - Variação da Pressão Muscular Mínima (Pmus_min)")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Pmus_min [cmH2O]")
    plt.plot(t, np.array(y_int["Pmus_min"]), color="r", label="Pmus_min")
    plt.legend(loc="upper left")
    
    plt.show()