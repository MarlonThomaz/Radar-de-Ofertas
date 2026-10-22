def formatar_oferta(produto):
    nome = produto.get("nome")
    preco = float(produto.get("preco", 0))
    desconto = float(produto.get("desconto", 0))
    preco_antigo = produto.get("preco_antigo")
    link = produto.get("url_afiliado") or produto.get("url")
    
    if preco_antigo:
        preco_antigo = float(preco_antigo)

        mensagem = (
            f"🔥 OFERTA SHOPEE!\n\n"
            f"🛍️ {nome}\n\n"
            f"~~R$ {preco_antigo:.2f}~~\n"
            f"💰 Por apenas R$ {preco:.2f}\n"
            f"🔥 {desconto:.0f}% OFF!\n\n"
            f"🛒 Aproveite!"
        )

    else:
        mensagem = (
            f"🔥 OFERTA SHOPEE!\n\n"
            f"🛍️ {nome}\n\n"
            f"💰 Por apenas R$ {preco:.2f}\n"
            f"🔥 {desconto:.0f}% OFF!\n\n"
            f"🛒 Aproveite!\n"
            f"👉 COMPRAR: {link}"
        )

    return mensagem