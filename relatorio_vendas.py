import json
from typing import List, Dict, Any, Optional
MESES = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]
NOME_ARQUIVO_JSON = "relatorio_vendas.json"
def coletar_vendas_manualmente(meses: List[str]) -> List[int]:
    print("\n--- Inserção Manual de Vendas ---")
    vendas_mensais = []
    for mes in meses:
        while True:
            try:
                vendas_str = input(f"Digite as vendas para {mes}: ")
                vendas_num = int(vendas_str)
                if vendas_num < 0:
                    print("Erro: O número de vendas não pode ser negativo. Tente novamente.")
                    continue
                vendas_mensais.append(vendas_num)
                break
            except ValueError:
                print("Erro: Entrada inválida. Por favor, digite um número inteiro.")
    return vendas_mensais
def carregar_vendas_de_json(nome_arquivo: str) -> Optional[List[int]]:
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            if "vendas_mensais" in dados and isinstance(dados["vendas_mensais"], list):
                print(f"Dados carregados com sucesso de '{nome_arquivo}'.")
                return dados["vendas_mensais"]
            else:
                print(f"Erro: O arquivo '{nome_arquivo}' não contém a chave 'vendas_mensais' válida.")
                return None
    except FileNotFoundError:
        print(f"Aviso: Arquivo '{nome_arquivo}' não encontrado. Começando com dados zerados.")
        return None
    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{nome_arquivo}' contém um JSON inválido.")
        return None
def analisar_dados(meses: List[str], vendas: List[int]) -> Dict[str, Any]:
    if not vendas or len(vendas) != len(meses):
        return {"media": 0, "acima_da_media": {}, "percentual": 0, "vendas_mensais": []}
    total_vendas = sum(vendas)
    media_anual = total_vendas / len(meses)
    meses_acima_da_media = {
        mes: venda for mes, venda in zip(meses, vendas) if venda > media_anual
    }
    percentual = (len(meses_acima_da_media) / len(meses)) * 100
    return {
        "media": media_anual,
        "acima_da_media": meses_acima_da_media,
        "percentual": percentual,
        "vendas_mensais": vendas
    }
def exibir_relatorio(analise: Dict[str, Any]):
    media = analise["media"]
    meses_acima = analise["acima_da_media"]
    percentual = analise["percentual"]
    print("\n--- Análise de Vendas Anual ---")
    print(f"Média anual de vendas: {media:.2f} unidades.")
    print("-" * 35)
    if not meses_acima:
        print("Nenhum mês teve vendas acima da média.")
    else:
        print("Meses com performance acima da média:")
        for mes, venda in meses_acima.items():
            print(f"  - {mes}: {venda} vendas")
    print(f"\nPercentual de meses acima da média: {percentual:.2f}%.")
    print("-" * 35)
def salvar_relatorio_em_json(nome_arquivo: str, dados_analise: Dict[str, Any]):
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados_analise, f, indent=4, ensure_ascii=False)
        print(f"Relatório salvo com sucesso em '{nome_arquivo}'.")
    except IOError as e:
        print(f"Erro ao salvar o arquivo '{nome_arquivo}': {e}")
def main():
    vendas_do_ano = []
    while True:
        escolha = input("Deseja (1) Inserir dados manualmente ou (2) Carregar de um arquivo JSON? ")
        if escolha == '1':
            vendas_do_ano = coletar_vendas_manualmente(MESES)
            break
        elif escolha == '2':
            vendas_do_ano = carregar_vendas_de_json(NOME_ARQUIVO_JSON)
            if vendas_do_ano is None:
                print("Não foi possível carregar os dados.")
                if input("Deseja inserir os dados manualmente? (s/n): ").lower() == 's':
                    vendas_do_ano = coletar_vendas_manualmente(MESES)
                    break
                else:
                    return
            else:
                break
        else:
            print("Opção inválida. Por favor, escolha 1 ou 2.")
    if not vendas_do_ano:
        print("Nenhum dado de venda para analisar. Encerrando.")
        return
    analise_de_vendas = analisar_dados(MESES, vendas_do_ano)
    exibir_relatorio(analise_de_vendas)
    if input("\nDeseja salvar este relatório em um arquivo JSON? (s/n): ").lower() == 's':
        salvar_relatorio_em_json(NOME_ARQUIVO_JSON, analise_de_vendas)
if __name__ == "__main__":
    main()