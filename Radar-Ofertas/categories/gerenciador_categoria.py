import json
import os

from categories.categorias_shopee import CATEGORIAS_SHOPEE

ARQUIVO_CONTROLE = "categories/controle_shopee.json"

MAX_PAGINAS = 3


def carregar_controle():
    if not os.path.exists(ARQUIVO_CONTROLE):
        return None

    with open(
        ARQUIVO_CONTROLE,
        "r",
        encoding="utf-8"
    ) as arquivo:
        return json.load(arquivo)


def salvar_controle(controle):
    with open(
        ARQUIVO_CONTROLE,
        "w",
        encoding="utf-8"
    ) as arquivo:
        json.dump(
            controle,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


def criar_primeira_busca():
    primeira_categoria = list(CATEGORIAS_SHOPEE.keys())[0]
    primeira_busca = CATEGORIAS_SHOPEE[primeira_categoria][0]

    return {
        "categoria": primeira_categoria,
        "busca": primeira_busca,
        "pagina": 1
    }


def escolher_busca_shopee():

    controle = carregar_controle()

    # Primeiro uso do Radar
    if not controle:
        controle = criar_primeira_busca()
        salvar_controle(controle)

        return (
            controle["categoria"],
            controle["busca"],
            controle["pagina"]
        )

    categoria_atual = controle["categoria"]
    busca_atual = controle["busca"]
    pagina_atual = controle["pagina"]

    # ==================================================
    # AVANÇA PARA A PRÓXIMA PÁGINA
    # ==================================================

    if pagina_atual < MAX_PAGINAS:

        pagina_atual += 1

        controle["pagina"] = pagina_atual

        salvar_controle(controle)

        return (
            categoria_atual,
            busca_atual,
            pagina_atual
        )

    # ==================================================
    # TERMINOU AS 3 PÁGINAS
    # VAI PARA A PRÓXIMA BUSCA
    # ==================================================

    todas_as_buscas = []

    for categoria, palavras in CATEGORIAS_SHOPEE.items():

        for palavra in palavras:

            todas_as_buscas.append(
                {
                    "categoria": categoria,
                    "busca": palavra
                }
            )

    indice_atual = None

    for indice, item in enumerate(todas_as_buscas):

        if (
            item["categoria"] == categoria_atual
            and item["busca"] == busca_atual
        ):
            indice_atual = indice
            break

    # Se encontrou a busca atual,
    # pega a próxima
    if indice_atual is not None:

        proximo_indice = indice_atual + 1

        # Se chegou ao final da lista,
        # volta para a primeira busca
        if proximo_indice >= len(todas_as_buscas):
            proximo_indice = 0

    else:
        proximo_indice = 0

    proxima_busca = todas_as_buscas[proximo_indice]

    controle = {
        "categoria": proxima_busca["categoria"],
        "busca": proxima_busca["busca"],
        "pagina": 1
    }

    salvar_controle(controle)

    return (
        controle["categoria"],
        controle["busca"],
        controle["pagina"]
    )


if __name__ == "__main__":

    categoria, busca, pagina = escolher_busca_shopee()

    print("🔎 GERENCIADOR DE CATEGORIAS SHOPEE")
    print("=" * 40)
    print(f"📂 Categoria: {categoria}")
    print(f"🔍 Busca: {busca}")
    print(f"📄 Página: {pagina}")