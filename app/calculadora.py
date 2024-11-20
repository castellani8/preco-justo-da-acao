"""Módulo para cálculo do preço justo de ações."""

from math import sqrt


def calcular_preco_graham(lpa: float, vpa: float, indice: float = 22.5) -> float:
    """Calcula o preço justo de uma ação usando o método de Benjamin Graham.

    Args:
        lpa (float): lucro por ação
        vpa (float): valor por ação
        indice (float, optional): índice de Graham. Defaults to 22.5.

    Returns:
        float: preço justo de Benjamin Graham
    """
    if lpa < 0 or vpa < 0:
        return 0

    return sqrt(indice * lpa * vpa)


def calcular_preco_bazin(valor_dy: float, dy_desejado: float = 0.06) -> float:
    """Calcula o preço justo de uma ação usando o método de Décio Bazin.

    Args:
        valor_dy (float): valor do "dividend yield"
        dy_desejado (float, optional): "dividend yield" desejado. Defaults to 0.06.

    Returns:
        float: preço justo de Décio Bazin
    """
    return 100 / (dy_desejado * 100) * valor_dy
