"""Módulo para obtenção de indicadores de ações."""

import requests
from bs4 import BeautifulSoup

__DEFAULT_TIMEOUT = 30


def obter_indicadores(ticker: str) -> dict:
    """Obter indicadores do site Fundamentus.

    Args:
        ticker (str): ticker (código de negociação) da ação

    Returns:
        dict: objeto que contém os indicadores
    """
    url = f"http://www.fundamentus.com.br/detalhes.php?papel={ticker}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers, timeout=__DEFAULT_TIMEOUT)
    soup = BeautifulSoup(response.text, "html.parser")

    data = {}
    table_rows = soup.find_all("tr")
    for row in table_rows:
        cols = row.find_all("td")
        if len(cols) == 6:
            keys = [0, 2, 4]
        elif len(cols) == 4:
            keys = [0, 2]
        else:
            continue
        for col in keys:
            key = cols[col].text.strip().replace("?", "")
            value = cols[col + 1].text.strip().replace(".", "").replace(",", ".")
            data[key] = value

    return data
