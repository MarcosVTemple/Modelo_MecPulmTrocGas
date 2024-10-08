import os
import json

from models.main_integracao import Integracao
from functions.plot_integracao import _plot, plot_dpoc_unico

if __name__ == "__main__":
    try:
        with open('input.json', "r") as input_json:
            input_dict = json.load(input_json)
            os.environ["save_figures"] = input_dict["save_figures"]
            os.environ["save_data"] = input_dict["save_data"]
            os.environ["tempo_simulacao"] = input_dict["tempo_simulacao"]
            os.environ["modo_ventilacao"] = input_dict["modo_ventilacao"]
            os.environ["modo_atividade"] = input_dict["modo_atividade"]
        
        print("Iniciando sistema integrado")
        int_obj = Integracao(resistencia_alveolar=40, fator_difusao=0.9)
        int_obj.run_integracao()
        int_obj.plot_integracao()
        
        
        
        # int_resistencia_obj = Integracao(resistencia_alveolar=40)
        # int_resistencia_obj.run_integracao()
        
        # int_difusao_obj = Integracao(fator_difusao=0.9)
        # int_difusao_obj.run_integracao()
        
        # int_ambos_obj = Integracao(resistencia_alveolar=40, fator_difusao=0.9)
        # int_ambos_obj.run_integracao()
        
        # int_obj = Integracao()
        # int_obj.run_integracao()
        
        # _plot(int_resistencia_obj, int_difusao_obj, int_ambos_obj, int_obj)
        # plot_dpoc_unico(int_ambos_obj, label="ambos")
        # int_ambos_obj.x_tg.to_csv(
        #         "temp/dpoc/dpoc_troca_gases_variaveis_estado_dt.csv",
        #         sep=";",
        #         index=False
        #     )
    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário")
