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
        
        resistencia_alveolar = 40
        fator_difusao = 0.9
        
        
        print("Simulação com aumento de RbA")
        # int_resistencia_obj = Integracao(resistencia_alveolar=resistencia_alveolar)
        int_resistencia_obj = Integracao(resistencia_alveolar=resistencia_alveolar, comparacoes="RbA")
        int_resistencia_obj.run_integracao()
        # with open("comparacoes_RbA.txt", "w") as f:
        #     f.write(f"Valores finais de nmols:\n{int_resistencia_obj.x_tg.tail(1).to_dict(orient='records')}")

        print("Simulação com redução de difusão")
        # int_difusao_obj = Integracao(fator_difusao=fator_difusao)
        int_difusao_obj = Integracao(fator_difusao=fator_difusao, comparacoes="difusao")
        int_difusao_obj.run_integracao()
        # with open("comparacoes_difusao.txt", "w") as f:
        #     f.write(f"Valores finais de nmols:\n{int_difusao_obj.x_tg.tail(1).to_dict(orient='records')}")
        
        print("Simulação com ambos")
        # int_ambos_obj = Integracao(resistencia_alveolar=resistencia_alveolar, fator_difusao=fator_difusao)
        int_ambos_obj = Integracao(resistencia_alveolar=resistencia_alveolar, fator_difusao=fator_difusao, comparacoes="ambos")
        int_ambos_obj.run_integracao()
        # with open("comparacoes_ambos.txt", "w") as f:
        #     f.write(f"Valores finais de nmols:\n{int_ambos_obj.x_tg.tail(1).to_dict(orient='records')}")
        
        print("Simulação sem modificacoes")
        # int_obj = Integracao()
        int_obj = Integracao(comparacoes="normal")
        int_obj.run_integracao()
        # with open("comparacoes_normal.txt", "w") as f:
        #     f.write(f"Valores finais de nmols:\n{int_obj.x_tg.tail(1).to_dict(orient='records')}")
        
        _plot(
            object_ra=int_resistencia_obj, 
            object_dif=int_difusao_obj, 
            object_both=int_ambos_obj, 
            object_normal=int_obj
        )
        
        # plot_dpoc_unico(int_obj, label="difusao")
        
        # int_ambos_obj.x_tg.to_csv(
        #         "temp/dpoc/dpoc_troca_gases_variaveis_estado_dt.csv",
        #         sep=";",
        #         index=False
        #     )
    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário")
