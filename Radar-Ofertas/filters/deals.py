def oferta_valida(preco_antigo, preco_novo, desconto_minimo=30):
    desconto = ((preco_antigo - preco_novo) / preco_antigo) * 100

    return desconto >= desconto_minimo