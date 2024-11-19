import os
import json

from models.main_integracao import Integracao
from functions.plot_integracao import _plot, plot_dpoc_unico

if __name__ == "__main__":
    try:
        with open("input.json", "r") as input_json:
            input_dict = json.load(input_json)
            os.environ["save_figures"] = input_dict["save_figures"]
            os.environ["save_data"] = input_dict["save_data"]
            os.environ["tempo_simulacao"] = input_dict["tempo_simulacao"]
            os.environ["modo_ventilacao"] = str(input_dict["modo_ventilacao"]).lower()
            os.environ["modo_atividade"] = str(input_dict["modo_atividade"]).lower()

        print("Iniciando execução do sistema integrado")
        print(
            f"\tModo de ventilação: {input_dict['modo_ventilacao']}\n\tAtividade: {input_dict['modo_atividade']}\n\tDuração: {input_dict['tempo_simulacao']} segundos"
        )

        if input_dict["modo_ventilacao"] == "normal":
            integracao_object = Integracao()
        elif input_dict["modo_ventilacao"] == "dpoc":
            resistencia_alveolar = 40
            fator_difusao = 0.9
            integracao_object = Integracao(
                resistencia_alveolar=resistencia_alveolar, fator_difusao=fator_difusao
            )

        integracao_object.run_integracao()
        integracao_object.plot_integracao()
    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário")
