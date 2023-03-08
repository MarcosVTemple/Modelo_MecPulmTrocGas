import os

from modelos.main_mec_pulm import MecanicaPulmonar
from modelos.main_troc_gas import TrocaGases
from modelos.main_integracao import Integracao


if __name__ == "__main__":
    try:
        os.environ["modo_ventilacao"] = "normal"
        # os.environ["modo_ventilacao"] = "apneia"
        os.environ["save_figures"] = input("Salvar figuras? [TRUE/FALSE]\n->").upper()
        os.environ["save_data"] = input("Salvar dados? [TRUE/FALSE]\n->").upper()
        os.environ["tempo_simulacao"] = input("Tempo de simulação do sistema? Ex.: 24 [segundos]\n->")

        # print("Iniciando Mecanica Pulmonar")
        # mec_pulm_obj = MecanicaPulmonar()
        # mec_pulm_obj.run_mecanica_pulmonar()
        # mec_pulm_obj.plot_mecanica_pulmonar()

        # print("Iniciando Troca de Gases")
        # troc_gas_obj = TrocaGases()
        # troc_gas_obj.run_troca_gases()
        # troc_gas_obj.plot_troca_gases()
        
        print("Iniciando sistema integrado")
        troc_gas_obj = Integracao()
        troc_gas_obj.run_integracao()
        troc_gas_obj.plot_integracao()
    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário")
