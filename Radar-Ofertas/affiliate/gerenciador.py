from affiliate.shopee import gerar_link as gerar_link_shopee_api
from config import SHOPEE_APP_ID, SHOPEE_SECRET


def gerar_link_afiliado(produto):
    plataforma = produto.get("plataforma")

    if plataforma == "shopee":
        return gerar_link_shopee(produto)

    elif plataforma == "mercadolivre":
        return gerar_link_mercadolivre(produto)

    elif plataforma == "temu":
        return gerar_link_temu(produto)

    elif plataforma == "magalu":
        return gerar_link_magalu(produto)

    return produto.get("url")


def gerar_link_shopee(produto):
    return gerar_link_shopee_api(
        produto,
        SHOPEE_APP_ID,
        SHOPEE_SECRET
    )


def gerar_link_mercadolivre(produto):
    return produto.get("url")


def gerar_link_temu(produto):
    return produto.get("url")


def gerar_link_magalu(produto):
    return produto.get("url")