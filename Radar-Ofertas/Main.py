from collectors.shopee import coletar_produtos
from filters.deals import oferta_valida, pontuar_oferta, oferta_top
from database import criar_tabela, adicionar_produto
from categories.gerenciador_categoria import escolher_busca_shopee
from formater.oferta_shopee import formatar_oferta
from affiliate.gerenciador import gerar_link_afiliado
from filters.filtro_publicacao import pode_publicar
from filters.deuplicados import remover_duplicados_semanticos
from datetime import datetime


def executar_radar():
    print("=" * 50)
    print("🚀 RADAR DE OFERTAS")
    print("=" * 50)

    criar_tabela()

    print("\n🔎 Buscando produtos na Shopee...")

    categoria, busca, pagina = escolher_busca_shopee()
    print(f"📂 Categoria: {categoria}")
    print(f"🔍 Busca: {busca}")

    print("\n🛒 Buscando produtos na Shopee...")

    produtos = coletar_produtos(
        keyword=busca,
        sort_type=1,
        page=pagina,
        limit=50
    )

    print(f"📂 Categoria: {categoria}")
    print(f"🔍 Busca: {busca}")
    print(f"📄 Página: {pagina}")
    print(f"📦 Produtos encontrados: {len(produtos)}")

    # Remove produtos duplicados pelo item_id
    produtos_unicos = {}

    for produto in produtos:
        item_id = produto.get("item_id")

        if item_id not in produtos_unicos:
            produtos_unicos[item_id] = produto

    produtos = list(produtos_unicos.values())
    # Remove produtos semanticamente duplicados
    quantidade_antes = len(produtos)

    produtos = remover_duplicados_semanticos(produtos)

    quantidade_depois = len(produtos)

    print(
    f"🧠 Duplicatas semânticas removidas: "
    f"{quantidade_antes - quantidade_depois}")

    print(
    f"🧹 Produtos únicos após limpeza: "
    f"{quantidade_depois}")

    print(f"🧹 Produtos únicos: {len(produtos)}")

    ofertas_boas = []
    ofertas_top = []

    for produto in produtos:

        if oferta_valida(produto):

            produto["pontuacao"] = pontuar_oferta(produto)

            if oferta_top(produto):
                produto["status"] = "🔥 TOP"
                ofertas_top.append(produto)
            else:
                produto["status"] = "⏸️ SEGURAR"

            ofertas_boas.append(produto)

    # Ordena as ofertas da maior pontuação para a menor
    ofertas_boas.sort(
        key=lambda produto: produto["pontuacao"],
        reverse=True
    )

    print(f"✅ Ofertas aprovadas: {len(ofertas_boas)}")

    if not ofertas_boas:
        print("⚠️ Nenhuma oferta passou pelo filtro.")
        return

    print("\n🏆 RANKING DAS OFERTAS:")

    for posicao, produto in enumerate(ofertas_boas, start=1):

        print(
            f"{posicao}º - "
            f"{produto['pontuacao']} pontos - "
            f"{produto['status']} - "
            f"{produto['nome']}"
        )

        print(
            f"   🔻 Desconto: "
            f"{produto['pontos_desconto']:.1f} pontos"
        )

        print(
            f"   🛒 Vendas: "
            f"{produto['pontos_vendas']:.1f} pontos"
        )

        print(
            f"   ⭐ Avaliação: "
            f"{produto['pontos_avaliacao']:.1f} pontos"
        )

        print(
            f"   💰 Comissão: "
            f"{produto['pontos_comissao']:.1f} pontos "
            f"({produto['comissao']}%)"
        )

    print("\n🔥 RESUMO DO RADAR")
    print(f"🔥 Ofertas TOP: {len(ofertas_top)}")

    print(
        f"⏸️ Ofertas para segurar: "
        f"{len(ofertas_boas) - len(ofertas_top)}"
    )

    print("\n💾 Salvando ofertas no banco...")

    data_atual = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )

    novos = 0
    sem_alteracao = 0
    quedas = 0
    ofertas_com_queda = []

    for produto in ofertas_boas:

        resultado = adicionar_produto(
            produto,
            data_atual
        )

        if resultado == "novo":
            novos += 1

        elif resultado == "sem_alteracao":
            sem_alteracao += 1

        elif resultado == "queda":
            quedas += 1
            ofertas_com_queda.append(produto)

    if ofertas_com_queda:

        print("\n📉 QUEDAS DE PREÇO DETECTADAS:")

        for produto in ofertas_com_queda:

            print(
                f"📉 {produto['nome']}"
            )

            print(
                f"💰 Preço atual: "
                f"R$ {produto['preco']:.2f}"
            )

            print(
                f"🔥 Pontuação: "
                f"{produto['pontuacao']} pontos"
            )

            print("-" * 50)

    # ==================================================
    # FILTRO DE PUBLICAÇÃO
    # ==================================================

    ofertas_publicadas = []

    print("\n📱 PRÉVIA DAS MENSAGENS:")

    for produto in ofertas_top:

        if pode_publicar(produto):

            print(
                f"\n✅ Aprovada para publicação:"
            )
            print(f"🛍️ {produto['nome']}")

            produto["url_afiliado"] = gerar_link_afiliado(
                produto
            )

            mensagem = formatar_oferta(produto)

            ofertas_publicadas.append(produto)

            print("\n" + "-" * 50)
            print(mensagem)
            print("-" * 50)

        else:

            print(
                f"\n🚫 TOP bloqueada pelo filtro de publicação:"
            )
            print(f"🛍️ {produto['nome']}")

    print("\n🎯 RESUMO DA PUBLICAÇÃO")
    print(
        f"🔥 Ofertas TOP: "
        f"{len(ofertas_top)}"
    )

    print(
        f"📱 Aprovadas para publicação: "
        f"{len(ofertas_publicadas)}"
    )

    print(
        f"🚫 Bloqueadas pelo filtro: "
        f"{len(ofertas_top) - len(ofertas_publicadas)}"
    )

    print("\n" + "=" * 50)
    print(
        f"🎯 Novas ofertas adicionadas: "
        f"{novos}"
    )

    print(
        f"🔄 Ofertas sem alteração: "
        f"{sem_alteracao}"
    )

    print(
        f"🔻 Ofertas com queda: "
        f"{quedas}"
    )

    print("=" * 50)


if __name__ == "__main__":
    executar_radar()