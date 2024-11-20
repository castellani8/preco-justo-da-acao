"""Módulo para obter fundamentos de ações e calcular o preço justo."""

import sys

from .fundamentus import obter_indicadores
from .calculadora import calcular_preco_bazin, calcular_preco_graham


def main():
    """Inicializar a aplicação."""
    if len(sys.argv) == 1:
        ticker = input("Digite o ticker do ativo: ").upper()
    else:
        ticker = sys.argv[1].upper()

    indicadores = obter_indicadores(ticker)

    lpa = float(indicadores.get("LPA", 0))
    vpa = float(indicadores.get("VPA", 0))
    cotacao = float(indicadores.get("Cotação", 0))
    dy = float(indicadores.get("Div. Yield", "0").strip("%")) / 100
    valor_dy = cotacao * dy

    indice_graham = 22.5
    dy_bazin = 0.08

    preco_graham = calcular_preco_graham(lpa, vpa, indice_graham)
    preco_bazin = calcular_preco_bazin(valor_dy, dy_bazin)

    print("-" * 40)
    print(f"Cotação: R$ {cotacao:.2f}")
    print(f"DY: {dy*100:.2f}%")
    print(f"LPA: R$ {lpa:.2f}")
    print(f"VPA: R$ {vpa:.2f}")
    print("-" * 40)
    print(f"Índice de Graham: {indice_graham:.2f}")
    print(f"DY de Bazin escolhido: {dy_bazin*100:.2f}%")
    print("-" * 40)
    print(f"Preço justo segundo Benjamin Graham: R$ {preco_graham:.2f}")
    print(f"Preço justo segundo Décio Bazin: R$ {preco_bazin:.2f}")


if __name__ == "__main__":
    main()
