def oferta_valida(produto, desconto_minimo=30):
    """
    Verifica se um produto atende aos critérios mínimos
    para ser considerado uma boa oferta.
    """

    desconto = float(produto.get("desconto", 0))
    vendas = int(produto.get("vendas", 0))
    avaliacao = float(produto.get("avaliacao", 0))

    if desconto < desconto_minimo:
        return False

    if vendas < 100:
        return False

    if avaliacao < 4.0:
        return False

    return True


def pontuar_oferta(produto):
    """
    Calcula uma pontuação de 0 a 100
    para determinar a qualidade da oferta.
    """

    desconto = float(produto.get("desconto", 0))
    vendas = int(produto.get("vendas", 0))
    avaliacao = float(produto.get("avaliacao", 0))
    comissao = float(produto.get("comissao", 0))

    # -------------------------
    # DESCONTO - até 40 pontos
    # -------------------------

    pontos_desconto = min(desconto / 2.5, 40)

    # -------------------------
    # VENDAS - até 30 pontos
    # -------------------------

    if vendas >= 10000:
        pontos_vendas = 30
    elif vendas >= 5000:
        pontos_vendas = 25
    elif vendas >= 1000:
        pontos_vendas = 20
    elif vendas >= 500:
        pontos_vendas = 15
    elif vendas >= 100:
        pontos_vendas = 10
    else:
        pontos_vendas = 0

    # -------------------------
    # AVALIAÇÃO - até 20 pontos
    # -------------------------

    pontos_avaliacao = min(
        avaliacao / 5 * 20,
        20
    )

    # -------------------------
    # COMISSÃO - até 10 pontos
    # -------------------------

    if comissao >= 10:
        pontos_comissao = 10
    elif comissao >= 5:
        pontos_comissao = 8
    elif comissao >= 3:
        pontos_comissao = 6
    elif comissao >= 1:
        pontos_comissao = 4
    else:
        pontos_comissao = 0

    # -------------------------
    # TOTAL
    # -------------------------

    produto["pontos_desconto"] = pontos_desconto
    produto["pontos_vendas"] = pontos_vendas
    produto["pontos_avaliacao"] = pontos_avaliacao
    produto["pontos_comissao"] =  pontos_comissao 


    pontuacao = (
        pontos_desconto
        + pontos_vendas
        + pontos_avaliacao
        + pontos_comissao
    )

    return round(min(pontuacao, 100), 2)

def oferta_top(produto, pontuacao_minima=65):
    """
    Verifica se a oferta tem pontuação suficiente
    para ser considerada uma oferta TOP.
    """

    pontuacao = pontuar_oferta(produto)

    return pontuacao >= pontuacao_minima