import requests
from bs4 import BeautifulSoup
from math import sqrt


def obter_indicadores_fundamentus(ticker):
    url = f"http://www.fundamentus.com.br/detalhes.php?papel={ticker}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
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


def calcular_preco_graham(lpa, vpa, indice=22.5):
    if lpa < 0 or vpa < 0:
        return 0

    return sqrt(indice * lpa * vpa)


def calcular_preco_bazin(valor_dy, dy_desejado=0.06):
    return 100 / (dy_desejado * 100) * valor_dy


def main():
    ticker = input("Digite o ticker da ação: ").upper()
    data = obter_indicadores_fundamentus(ticker)

    lpa = float(data.get("LPA", 0))
    vpa = float(data.get("VPA", 0))
    cotacao = float(data.get("Cotação", 0))
    dy = float(data.get("Div. Yield", "0").strip("%")) / 100
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
