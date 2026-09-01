def criar_mensagem(oferta):

    produto, preco_antigo, preco_novo, desconto, link = oferta

    mensagem = f"""
🔥 OFERTA ENCONTRADA!

🛍️ {produto}

💰 De: R$ {preco_antigo:.2f}
🔥 Por: R$ {preco_novo:.2f}

🏷️ DESCONTO: {desconto:.0f}% OFF

🛒 COMPRAR:
{link}
"""

    return mensagem