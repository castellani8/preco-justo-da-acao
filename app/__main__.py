import pandas as pd
from fundamentus import obter_indicadores
from calculadora import calcular_preco_bazin, calcular_preco_graham

def main():
    # Carregar dados do arquivo CSV
    file_path = "table.csv"
    df = pd.read_csv(file_path)

    # Preprocessar o DataFrame
    df = preprocessa_dataframe(df)

    # Adicionar análises
    df = analisa_acoes(df)

    # Exibir resultados
    print(df)
    df.to_csv("analise_resultado.csv", index=False)


def preprocessa_dataframe(df):
    """Converte colunas relevantes e remove caracteres desnecessários."""
    for col in ["Preço médio", "Preço atual", "Total investido", "Total atual", "Ganho", "% Ganho"]:
        if col in df.columns:
            # Remove "R$" e "%" e ajusta os separadores de milhar/ponto
            df[col] = (
                df[col]
                .str.replace("R$", "", regex=False)  # Remove o símbolo R$
                .str.replace("%", "", regex=False)   # Remove o símbolo %
                .str.replace(".", "", regex=False)   # Remove pontos (separadores de milhar)
                .str.replace(",", ".", regex=False)  # Substitui vírgula por ponto (decimal)
                .str.strip()                         # Remove espaços extras
            )
            # Converte valores válidos para float
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def analisa_acoes(df):
    """Analisa as ações e calcula os preços justos de acordo com Graham e Bazin."""
    acoes = df["Ativo"].unique()

    resultados = []
    for ativo in acoes:
        if ativo.startswith("CDB") or ativo.startswith("Trend") or ativo.startswith("25 ativos"):
            # Ignorar ativos que não são ações
            continue

        indicadores = obter_indicadores(ativo)

        # Obter valores relevantes
        lpa = float(indicadores.get("LPA", 0))
        vpa = float(indicadores.get("VPA", 0))
        cotacao = float(indicadores.get("Cotação", 0))
        dy = float(indicadores.get("Div. Yield", "0").strip("%")) / 100
        valor_dy = cotacao * dy

        # Critérios de Graham e Bazin
        indice_graham = 22.5
        dy_bazin = 0.08

        preco_graham = calcular_preco_graham(lpa, vpa, indice_graham)
        preco_bazin = calcular_preco_bazin(valor_dy, dy_bazin)

        # Determinar ação
        preco_atual = df.loc[df["Ativo"] == ativo, "Preço atual"].values[0]
        if preco_atual < preco_graham:
            recomendacao = "Compra"
        elif preco_atual > preco_bazin:
            recomendacao = "Venda"
        else:
            recomendacao = "Manter"

        resultados.append({
            "Ativo": ativo,
            "Preço Atual": f"R$ {preco_atual:.2f}",
            "DY": f"{dy * 100}%",
            "Preço Graham": f"R$ {preco_graham:.2f}",
            "Preço Bazin": f"R$ {preco_bazin:.2f}",
            "Recomendação": recomendacao
        })

    return pd.DataFrame(resultados)


if __name__ == "__main__":
    main()
