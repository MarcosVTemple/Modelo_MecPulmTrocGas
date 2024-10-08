import os
import time
import numpy as np
import matplotlib.pyplot as plt

TEST_CASE = ""


def plot_dpoc_unico(object_ra, label=""):
    plt.figure(1)
    plt.title("Volume do espaço morto")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Volume [L]")
    plt.plot(object_ra.t[1:], np.array(object_ra.y_mp["VD"])[1:], color="r", label=label)
    plt.legend(loc="upper left")
    plt.savefig("temp/dpoc/VD")
    
    plt.figure(2)
    plt.title("Volume alveolar")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Volume [L]")
    plt.plot(object_ra.t[1:], np.array(object_ra.y_mp["VA"])[1:], color="r", label=label) 
    plt.legend(loc="upper left")
    plt.savefig("temp/dpoc/VA")
    
    plt.figure(3)
    plt.title("Vazão alveolar")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Volume [L/s]")
    plt.plot(object_ra.t[1:], np.array(object_ra.y_mp["VA_dot"])[1:], color="r", label=label)
    plt.legend(loc="upper left")
    plt.savefig("temp/dpoc/VA_dot")
    
    plt.figure(4)
    plt.title("Pressão parcial de oxigenio nos capilares")
    plt.xlabel("Tempo [s]")
    plt.ylabel("P parcial [mmHg]")
    plt.plot(object_ra.t[1:], np.array(object_ra.y_tg["P_cap_O2"])[1:], color="r", label=label)
    plt.legend(loc="upper left")
    plt.savefig("temp/dpoc/PaO2")
    plt.show()
    

def _plot(object_ra, object_dif, object_both, object_normal):
    plt.figure(1)
    plt.title("Volume do espaço morto")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Volume [L]")
    plt.plot(object_both.t[1:], np.array(object_ra.y_mp["VD"])[1:], color="r", label="RbA", marker = 'o')
    plt.plot(object_both.t[1:], np.array(object_dif.y_mp["VD"])[1:], color="b", label="difusao", marker = '+')
    plt.plot(object_both.t[1:], np.array(object_both.y_mp["VD"])[1:], color="g", label="both")
    plt.plot(object_both.t[1:], np.array(object_normal.y_mp["VD"])[1:], color="k", label="normal")
    plt.legend(loc="upper left")
    plt.savefig("temp/dpoc/VD")
    
    plt.figure(2)
    plt.title("Volume alveolar")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Volume [L]")
    plt.plot(object_both.t[1:], np.array(object_ra.y_mp["VA"])[1:], color="r", label="RbA", marker = 'o')
    plt.plot(object_both.t[1:], np.array(object_dif.y_mp["VA"])[1:], color="b", label="difusao", marker = '+')
    plt.plot(object_both.t[1:], np.array(object_both.y_mp["VA"])[1:], color="g", label="both")
    plt.plot(object_both.t[1:], np.array(object_normal.y_mp["VA"])[1:], color="k", label="normal")
    plt.legend(loc="upper left")
    plt.savefig("temp/dpoc/VA")
    
    plt.figure(3)
    plt.title("Vazão alveolar")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Volume [L/s]")
    plt.plot(object_both.t[1:], np.array(object_ra.y_mp["VA_dot"])[1:], color="r", label="RbA", marker = 'o')
    plt.plot(object_both.t[1:], np.array(object_dif.y_mp["VA_dot"])[1:], color="b", label="difusao", marker = '+')
    plt.plot(object_both.t[1:], np.array(object_both.y_mp["VA_dot"])[1:], color="g", label="both")
    plt.plot(object_both.t[1:], np.array(object_normal.y_mp["VA_dot"])[1:], color="k", label="normal")
    plt.legend(loc="upper left")
    plt.savefig("temp/dpoc/VA_dot")
    
    plt.figure(4)
    plt.title("Pressão parcial de oxigenio nos capilares")
    plt.xlabel("Tempo [s]")
    plt.ylabel("P parcial [mmHg]")
    plt.plot(object_both.t[1:], np.array(object_ra.y_tg["P_cap_O2"])[1:], color="r", label="RbA", marker = 'o')
    plt.plot(object_both.t[1:], np.array(object_dif.y_tg["P_cap_O2"])[1:], color="b", label="difusao", marker = '+')
    plt.plot(object_both.t[1:], np.array(object_both.y_tg["P_cap_O2"])[1:], color="g", label="both")
    plt.plot(object_both.t[1:], np.array(object_normal.y_tg["P_cap_O2"])[1:], color="k", label="normal")
    plt.legend(loc="upper left")
    plt.savefig("temp/dpoc/PaO2")
    plt.show()
    


def plot_int(t, x_tg, y_tg, u_tg, x_mp, y_mp, u_mp, y_int):
    timestamp = str(int(round(time.time() * 1000)))
    result_folder = "int"
    if os.getenv("modo_ventilacao", default="") == 'dpoc':
        result_folder = "dpoc"
    ### mp 
    plt.figure(1)
    # plt.title("Mecânica Pulmonar - Pressões")
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
            f"temp/{result_folder}/figures/1_pressoes_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}_{timestamp}"
        )

    plt.figure(2)
    # plt.title("Mecânica Pulmonar - Fluxos")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Fluxo [L/s]")
    plt.plot(t, np.array(y_mp["V_dot"]), color="r", label="V_dot")
    plt.plot(t, np.array(y_mp["VA_dot"]), color="b", label="VA_dot")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/{result_folder}/figures/2_fluxos_"
            f"{os.getenv('modo_ventilacao', 'normal')}_"
            f"{os.getenv('modo_atividade', 'repouso')}_{timestamp}"
        )

    plt.figure(3)
    # plt.title("Mecânica Pulmonar - Volumes")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Volume [L]")
    plt.plot(t[1:], np.array(y_mp["VA"])[1:], color="k", label="VA")
    plt.plot(t[1:], np.array(y_mp["V"])[1:], label="V")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/{result_folder}/figures/3_volumes_"
            f"{os.getenv('modo_ventilacao', 'normal')}_"
            f"{os.getenv('modo_atividade', 'repouso')}_{timestamp}"
        )

    plt.figure(4)
    # plt.title("Mecânica Pulmonar - Volumes")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Volume [L]")
    plt.plot(t[1:], np.array(y_mp["Vl"])[1:], color="r", label="Vl")
    plt.plot(t[1:], np.array(y_mp["Vtr"])[1:], color="b", label="Vtr")
    plt.plot(t[1:], np.array(y_mp["Vb"])[1:], color="g", label="Vb")
    plt.plot(t[1:], np.array(y_mp["VD"])[1:], color="y", label="VD")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/{result_folder}/figures/4_volumes_saida_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}_{timestamp}"
        )

    plt.figure(5)
    # plt.title("Mecânica Pulmonar - Pressões de entrada")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Pressão [cmH2O]")
    plt.plot(t[1:], np.array(u_mp["Pmus"])[1:], color="r", label="Pmus")
    plt.plot(t[1:], np.array(u_mp["dPmus"])[1:], color="k", label="dPmus")
    # plt.plot(t, derivada_pmus, color="b", label="derivada_pmus")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/{result_folder}/figures/5_pressoes_entrada_"
            f"{os.getenv('modo_ventilacao','normal')}"
            f"_{os.getenv('modo_atividade','repouso')}_{timestamp}"
        )
    # plt.show()

    
    ### tg
    # plt.figure(6)
    # # plt.title("Troca de Gases - nº de Mols dos Gases no Compartimento Alveolar")
    # plt.xlabel("Tempo [s]")
    # plt.ylabel("nº de Mols [mmol]")
    # plt.plot(t, np.array(x_tg["n_A_O2"]), color="r", label="n_A_O2")
    # plt.plot(t, np.array(x_tg["n_A_CO2"]), color="b", label="n_A_CO2")
    # plt.plot(t, np.array(x_tg["n_A_N2"]), color="g", label="n_A_N2")
    # plt.legend(loc="upper left")
    # if os.getenv("save_figures", default="") == 'TRUE':
    #     plt.savefig(
    #         f"temp/{result_folder}/figures/1_mols_alveolo_"
    #         f"{os.getenv('modo_ventilacao','normal')}_"
    #         f"{os.getenv('modo_atividade','repouso')}_{timestamp}"
    #     ) 
    # plt.show()

    # plt.figure(7)
    # # plt.title("Troca de Gases - nº de Mols dos Gases no Compartimento Capilar")
    # plt.xlabel("Tempo [s]")
    # plt.ylabel("nº de Mols [mmol]")
    # plt.plot(t, np.array(x_tg["n_cap_O2"]), color="r", label="n_cap_O2")
    # plt.plot(t, np.array(x_tg["n_cap_CO2"]), color="k", label="n_cap_CO2")
    # plt.legend(loc="upper left")
    # if os.getenv("save_figures", default="") == 'TRUE':
    #     plt.savefig(
    #         f"temp/{result_folder}/figures/2_mols_capilar_"
    #         f"{os.getenv('modo_ventilacao','normal')}_"
    #         f"{os.getenv('modo_atividade','repouso')}_{timestamp}"
    #     )

    # plt.figure(8)
    # # plt.title("Troca de Gases - nº de Mols dos Gases no Compartimento Tecidual")
    # plt.xlabel("Tempo [s]")
    # plt.ylabel("nº de Mols [mmol]")
    # plt.plot(t, np.array(x_tg["n_t_O2"]), color="r", label="n_t_O2")
    # plt.plot(t, np.array(x_tg["n_t_CO2"]), color="k", label="n_t_CO2")
    # plt.legend(loc="upper left")
    # if os.getenv("save_figures", default="") == 'TRUE':
    #     plt.savefig(
    #         f"temp/{result_folder}/figures/3_mols_tecidual_"
    #         f"{os.getenv('modo_ventilacao','normal')}_"
    #         f"{os.getenv('modo_atividade','repouso')}_{timestamp}"
    #     )

    # plt.figure(9)
    # # plt.title("Troca de Gases - Vazão Alveolar")
    # plt.xlabel("Tempo [s]")
    # plt.ylabel("Fluxo [L/s]")
    # plt.plot(t, np.array(u_tg["VA_dot"]), color="r", label="VA_dot")
    # plt.legend(loc="upper left")
    # if os.getenv("save_figures", default="") == 'TRUE':
    #     plt.savefig(
    #         f"temp/{result_folder}/figures/4_vazao_alveolo_"
    #         f"{os.getenv('modo_ventilacao','normal')}_"
    #         f"{os.getenv('modo_atividade','repouso')}_{timestamp}"
    #     )

    # plt.figure(10)
    # plt.title("Troca de Gases - Pressões Parciais dos Gases no Compartimento Alveolar")
    # plt.xlabel("Tempo [s]")
    # plt.ylabel("P parcial [mmHg]")
    # plt.plot(t, np.array(y_tg["P_A_O2"]), color="r", label="P_A_O2")
    # plt.plot(t, np.array(y_tg["P_A_CO2"]), color="b", label="P_A_CO2")
    # plt.plot(t, np.array(y_tg["P_A_N2"]), color="g", label="P_A_N2")
    # plt.legend(loc="upper left")
    # if os.getenv("save_figures", default="") == 'TRUE':
    #     plt.savefig(
    #         f"temp/{result_folder}/figures/5_pparcial_alveolo_"
    #         f"{os.getenv('modo_ventilacao','normal')}_"
    #         f"{os.getenv('modo_atividade','repouso')}"
    #     )

    # plt.figure(11)
    # plt.title("Troca de Gases - Pressões Parciais dos Gases no Compartimento Capilar")
    # plt.xlabel("Tempo [s]")
    # plt.ylabel("P parcial [mmHg]")
    # plt.plot(t, np.array(y_tg["P_cap_O2"]), color="r", label="P_cap_O2")
    # plt.plot(t, np.array(y_tg["P_cap_CO2"]), color="b", label="P_cap_CO2")
    # plt.legend(loc="upper left")
    # if os.getenv("save_figures", default="") == 'TRUE':
    #     plt.savefig(
    #         f"temp/{result_folder}/figures/6_pparcial_capilar_"
    #         f"{os.getenv('modo_ventilacao','normal')}_"
    #         f"{os.getenv('modo_atividade','repouso')}"
    #     )
        
    #### ALVEOLO + CAPILARES
    plt.figure(10)
    # plt.title("Troca de Gases - Pressões Parciais dos Gases nos Compartimentos Alveolar e Capilar")
    plt.xlabel("Tempo [s]")
    plt.ylabel("P parcial [mmHg]")
    plt.plot(t[1:], np.array(y_tg["P_A_O2"])[1:], color="r", label="P_A_O2", linestyle="dashed")
    plt.plot(t[1:], np.array(y_tg["P_A_CO2"])[1:], color="b", label="P_A_CO2", linestyle="dashed")
    plt.plot(t[1:], np.array(y_tg["P_cap_O2"])[1:], color="r", label="P_cap_O2", linestyle="dotted")
    plt.plot(t[1:], np.array(y_tg["P_cap_CO2"])[1:], color="b", label="P_cap_CO2", linestyle="dotted")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/{result_folder}/figures/6_pparcial_capilar_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}_"
            f"{TEST_CASE}_{timestamp}"
        )
    ####
    
        
    plt.figure(12)
    # plt.title("Controle - Variação da Frequência Respiratória (RR)")
    plt.xlabel("Tempo [s]")
    plt.ylabel("RR [inc/min]")
    plt.plot(t[1:], np.array(y_int["RR"])[1:], color="g", label="RR")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/{result_folder}/figures/7_variacao_frequencia_resp_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}_"
            f"{TEST_CASE}_{timestamp}"
        )
        
    plt.figure(13)
    # plt.title("Controle - Variação da Pressão Muscular Mínima (Pmus_min)")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Pmus_min [cmH2O]")
    plt.plot(t[1:], np.array(y_int["Pmus_min"])[1:], color="b", label="Pmus_min")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/{result_folder}/figures/13_variacao_pmusmin_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}_"
            f"{TEST_CASE}_{timestamp}"
        )
        
    plt.figure(14)
    # plt.title("Controle - Variação do Débito Cardíaco (Q_b)")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Q_b [L/min]")
    plt.plot(t[1:], np.array(y_int["Q_b"])[1:], color="r", label="Q_b")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/{result_folder}/figures/8_variacao_debito_cardiaco_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}_{timestamp}"
        )
        
    plt.figure(15)
    # plt.title("Volume do Espaço Morto (VD)")
    plt.xlabel("Tempo [s]")
    plt.ylabel("VD [L]")
    plt.plot(t[1:], np.array(y_mp["VD"])[1:], color="y", label="VD")
    plt.legend(loc="upper left")
    if os.getenv("save_figures", default="") == 'TRUE':
        plt.savefig(
            f"temp/{result_folder}/figures/15_volume_morto_"
            f"{os.getenv('modo_ventilacao','normal')}_"
            f"{os.getenv('modo_atividade','repouso')}_{timestamp}"
        )
    plt.show()
    
        
    pcapo2final = np.array(y_tg["P_cap_O2"])[-1]
    pcapco2final = np.array(y_tg["P_cap_CO2"])[-1]
    print(f"P_cap_O2: {pcapo2final}")
    print(f"P_cap_CO2: {pcapco2final}")