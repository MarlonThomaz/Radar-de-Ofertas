from bs4 import BeautifulSoup
from database import adicionar_oferta
from filters.deals import oferta_valida
from datetime import datetime


def converter_preco(preco):
    preco = preco.replace("R$", "")
    preco = preco.replace(".", "")
    preco = preco.replace(",", ".")

    return float(preco)


def analisar_ofertas():

    with open("produtos.html", "r", encoding="utf-8") as arquivo:
        pagina = arquivo.read()

    soup = BeautifulSoup(pagina, "html.parser")

    produtos = soup.find_all("div", class_="produto")

    print("\n--- ANALISANDO OFERTAS ---")

    for produto in produtos:

        nome = produto.find("h2").text.strip()

        preco_antigo = converter_preco(
            produto.find("p", class_="preco-antigo").text
        )

        preco_novo = converter_preco(
            produto.find("p", class_="preco-novo").text
        )

        link = produto.find("a")["href"]

        desconto = ((preco_antigo - preco_novo) / preco_antigo) * 100

        print("\nProduto:", nome)
        print("Desconto:", round(desconto, 2), "%")

        if oferta_valida(preco_antigo, preco_novo):

            print("✅ OFERTA APROVADA!")

            adicionar_oferta(
                nome,
                preco_antigo,
                preco_novo,
                desconto,
                link,
                datetime.now().strftime("%d/%m/%Y %H:%M")
            )

        else:

            print("❌ Oferta descartada.")