"""Módulo para obter fundamentos de ações e calcular o preço justo."""

import sys
import pandas as pd

from fundamentus import obter_indicadores
from calculadora import calcular_preco_bazin, calcular_preco_graham


def main():
    data = monta_dict()
    dataf = pd.DataFrame.from_dict(data)
    print(dataf)
    # """Inicializar a aplicação."""
    # if len(sys.argv) == 1:
    #     ticker = input("Digite o ticker do ativo: ").upper()
    # else:
    #     ticker = sys.argv[1].upper()

def monta_dict():
    data = {}
    for i in ['VALE3', 'PETR4']:
        indicadores = obter_indicadores(i)

        lpa = float(indicadores.get("LPA", 0))
        vpa = float(indicadores.get("VPA", 0))
        cotacao = float(indicadores.get("Cotação", 0))
        dy = float(indicadores.get("Div. Yield", "0").strip("%")) / 100
        valor_dy = cotacao * dy

        indice_graham = 22.5
        dy_bazin = 0.08

        preco_graham = calcular_preco_graham(lpa, vpa, indice_graham)
        preco_bazin = calcular_preco_bazin(valor_dy, dy_bazin)
        data[i] = {
            'Cotação': f"{cotacao:.2f}", 
            "DY": f"{dy*100:.2f}%",
            # "LPA": f"R$ {lpa:.2f}",
            # "VPA": f"VPA: R$ {vpa:.2f}",
            # "Índice de Graham": f"{indice_graham:.2f}",
            # "DY de Bazin escolhido": f"{dy_bazin*100:.2f}%",
            "Preço justo segundo Benjamin Graham": f"R$ {preco_graham:.2f}",
            "Preço justo segundo Décio Bazin": f"R$ {preco_bazin:.2f}"
        }
    return data
    
if __name__ == "__main__":
    main()
