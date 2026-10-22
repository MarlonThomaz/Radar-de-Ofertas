import hashlib
import json
import time
import requests

from config import SHOPEE_APP_ID, SHOPEE_SECRET


SHOPEE_API_URL = "https://open-api.affiliate.shopee.com.br/graphql"


def executar_query(query):
    """
    Executa uma query GraphQL autenticada na API da Shopee.
    """

    timestamp = str(int(time.time()))

    payload = {
        "query": query
    }

    payload_json = json.dumps(
        payload,
        separators=(",", ":"),
        ensure_ascii=False
    )

    signature_factor = (
        SHOPEE_APP_ID
        + timestamp
        + payload_json
        + SHOPEE_SECRET
    )

    signature = hashlib.sha256(
        signature_factor.encode("utf-8")
    ).hexdigest()

    headers = {
        "Authorization": (
            f"SHA256 Credential={SHOPEE_APP_ID}, "
            f"Timestamp={timestamp}, "
            f"Signature={signature}"
        ),
        "Content-Type": "application/json"
    }

    response = requests.post(
        SHOPEE_API_URL,
        headers=headers,
        data=payload_json,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    if "errors" in data:
        print("Erro da API Shopee:")
        print(data["errors"])
        return None

    return data


def buscar_produtos(
    keyword=None,
    sort_type=2,
    page=1,
    limit=10
):
    """
    Busca produtos/ofertas na Shopee.

    sort_type:
        1 = relevância
        2 = mais vendidos
        3 = maior preço
        4 = menor preço
        5 = maior comissão
    """

    argumentos = [
        f"sortType: {sort_type}",
        f"page: {page}",
        f"limit: {limit}"
    ]

    if keyword:
        keyword_json = json.dumps(
            keyword,
            ensure_ascii=False
        )

        argumentos.append(
            f"keyword: {keyword_json}"
        )

    query = f"""
query {{
    productOfferV2(
        {", ".join(argumentos)}
    ) {{
        nodes {{
            itemId
            commissionRate
            sellerCommissionRate
            shopeeCommissionRate
            commission
            priceMin
            priceMax
            sales
            productCatIds
            ratingStar
            priceDiscountRate
            imageUrl
            productName
            shopId
            shopName
            shopType
            productLink
            offerLink
            periodStartTime
            periodEndTime
        }}
        pageInfo {{
            page
            limit
            hasNextPage
        }}
    }}
}}
"""



    data = executar_query(query)

    if not data:
        return []

    try:
        return data["data"]["productOfferV2"]["nodes"]

    except (KeyError, TypeError):
        print("Resposta inesperada da Shopee:")
        print(data)
        return []


def transformar_produto(produto):
    """
    Converte o produto da Shopee
    para o formato padrão do Radar.
    """

    return {
        
        "item_id": produto.get("itemId"),
        "nome": produto.get("productName"),
        "preco": float(produto.get("priceMin", 0)),
        "desconto": produto.get("priceDiscountRate", 0),
        "comissao": float(produto.get("commission", 0)),
        "vendas": produto.get("sales", 0),
        "avaliacao": float(produto.get("ratingStar", 0)),
        "imagem": produto.get("imageUrl"),
        "url": produto.get("productLink"),
        "url_afiliado": produto.get("offerLink"),
        "plataforma": "shopee"
    }

def coletar_produtos(
    keyword=None,
    sort_type=2,
    page=1,
    limit=10
):
    """
    Busca produtos na Shopee
    e devolve todos no formato padrão do Radar.
    """

    produtos = buscar_produtos(
        keyword=keyword,
        sort_type=sort_type,
        page=page,
        limit=limit
    )

    produtos_formatados = []

    for produto in produtos:
        produto_formatado = transformar_produto(produto)
        produtos_formatados.append(produto_formatado)

    return produtos_formatados