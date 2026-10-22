import hashlib
import json
import time
import requests


SHOPEE_API_URL = "https://open-api.affiliate.shopee.com.br/graphql"


def gerar_link(produto, app_id, secret):
    url_produto = produto.get("url")

    if not url_produto:
        return None

    # Timestamp atual
    timestamp = str(int(time.time()))

    # Query GraphQL
    query = """
mutation {
    generateShortLink(input: {
        originUrl: %s
    }) {
        shortLink
    }
}
""" % json.dumps(url_produto, ensure_ascii=False)

    # Corpo da requisição
    payload = {
        "query": query
    }

    # JSON EXATO que será enviado
    payload_json = json.dumps(
        payload,
        separators=(",", ":"),
        ensure_ascii=False
    )

    # AppId + Timestamp + Payload + Secret
    signature_factor = (
        app_id
        + timestamp
        + payload_json
        + secret
    )

    # SHA256
    signature = hashlib.sha256(
        signature_factor.encode("utf-8")
    ).hexdigest()

    # Authorization
    authorization = (
        f"SHA256 Credential={app_id}, "
        f"Timestamp={timestamp}, "
        f"Signature={signature}"
    )

    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json"
    }

    # Envia para a Shopee
    response = requests.post(
        SHOPEE_API_URL,
        headers=headers,
        data=payload_json,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    # Erros GraphQL
    if "errors" in data:
        print("Erro da API Shopee:")
        print(data["errors"])
        return None

    try:
        return data["data"]["generateShortLink"]["shortLink"]

    except (KeyError, TypeError):
        print("Resposta inesperada da Shopee:")
        print(data)
        return None