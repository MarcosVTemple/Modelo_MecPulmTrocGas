import os
import json

from models.main_mec_pulm import MecanicaPulmonar
from models.main_troc_gas import TrocaGases
from models.main_integracao import Integracao


if __name__ == "__main__":
    try:
        with open('input.json', "r") as input_json:
            input_dict = json.load(input_json)
            os.environ["save_figures"] = input_dict["save_figures"]
            os.environ["save_data"] = input_dict["save_data"]
            os.environ["tempo_simulacao"] = input_dict["tempo_simulacao"]
            os.environ["modo_ventilacao"] = input_dict["modo_ventilacao"]
        
        print("Iniciando sistema integrado")
        int_obj = Integracao()
        int_obj.run_integracao()
        int_obj.plot_integracao()
    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário")
