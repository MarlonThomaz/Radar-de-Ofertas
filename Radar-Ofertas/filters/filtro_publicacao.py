def pode_publicar(produto):
    """
    Decide se uma oferta TOP pode ser publicada.
    """

    pontuacao = float(produto.get("pontuacao", 0))
    desconto = float(produto.get("desconto", 0))
    avaliacao = float(produto.get("avaliacao", 0))
    comissao = float(produto.get("comissao", 0))
    vendas = int(produto.get("vendas", 0))

    if pontuacao < 65:
        return False

    if desconto < 30:
        return False

    if avaliacao < 4.5:
        return False

    if vendas < 150:
        return False

    if comissao < 1:
        return False

    return True