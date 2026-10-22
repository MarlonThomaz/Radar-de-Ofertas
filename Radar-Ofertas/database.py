import sqlite3


BANCO = "data/ofertas.db"


def conectar():
    return sqlite3.connect(BANCO)


def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    # Cria a tabela caso ela ainda não exista
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ofertas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            preco_antigo REAL,
            preco_novo REAL,
            desconto REAL,
            link TEXT,
            data TEXT,
            enviada INTEGER DEFAULT 0
        )
    """)

    # Descobre quais colunas já existem
    cursor.execute("PRAGMA table_info(ofertas)")
    colunas_existentes = {
        coluna[1] for coluna in cursor.fetchall()
    }

    # Novas colunas do Radar
    novas_colunas = {
        "comissao": "REAL DEFAULT 0",
        "vendas": "INTEGER DEFAULT 0",
        "avaliacao": "REAL DEFAULT 0",
        "imagem": "TEXT",
        "plataforma": "TEXT",
        "url_original": "TEXT",
        "item_id": "INTEGER"
    }

    # Adiciona somente as que ainda não existem
    for coluna, tipo in novas_colunas.items():
        if coluna not in colunas_existentes:
            cursor.execute(
                f"ALTER TABLE ofertas ADD COLUMN {coluna} {tipo}"
            )

    conexao.commit()
    conexao.close()

    print("Banco de dados pronto!")


def adicionar_produto(produto, data):
    """
    Adiciona um produto padronizado pelo Radar.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    item_id = produto.get("item_id")
    nome = produto.get("nome")
    preco = float(produto.get("preco", 0))
    desconto = float(produto.get("desconto", 0))
    comissao = float(produto.get("comissao", 0))
    vendas = int(produto.get("vendas", 0))
    avaliacao = float(produto.get("avaliacao", 0))
    imagem = produto.get("imagem")
    url_original = produto.get("url")

    # Preferimos o link de afiliado
    link = produto.get("url_afiliado") or url_original

    plataforma = produto.get("plataforma")

    # Procura se esse produto já existe
    cursor.execute(
        """
        SELECT id, preco_novo
        FROM ofertas
        WHERE item_id = ?
        AND plataforma = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (item_id, plataforma)
    )

    oferta_existente = cursor.fetchone()

    # ==========================================
    # PRODUTO JÁ EXISTE
    # ==========================================

    if oferta_existente:

        oferta_id = oferta_existente[0]
        preco_anterior = float(oferta_existente[1])

        print(
            f"Produto já existe. "
            f"Preço anterior: R$ {preco_anterior:.2f}"
        )

        print(
            f"Preço atual: R$ {preco:.2f}"
        )

        # QUEDA DE PREÇO
        if preco < preco_anterior:

            print("📉 QUEDA DE PREÇO!")

            cursor.execute(
                """
                UPDATE ofertas
                SET
                    preco_antigo = preco_novo,
                    preco_novo = ?,
                    desconto = ?,
                    link = ?,
                    data = ?,
                    enviada = 0,
                    comissao = ?,
                    vendas = ?,
                    avaliacao = ?,
                    imagem = ?,
                    plataforma = ?,
                    url_original = ?
                WHERE id = ?
                """,
                (
                    preco,
                    desconto,
                    link,
                    data,
                    comissao,
                    vendas,
                    avaliacao,
                    imagem,
                    plataforma,
                    url_original,
                    oferta_id
                )
            )

            conexao.commit()

            print("💾 Nova queda de preço salva!")

            conexao.close()

            return "queda"

        # SEM QUEDA
        else:

            print("➡️ Sem queda de preço.")

            conexao.close()

            return "sem_alteracao"

    # ==========================================
    # PRODUTO NOVO
    # ==========================================

    cursor.execute(
        """
        INSERT INTO ofertas (
            produto,
            preco_antigo,
            preco_novo,
            desconto,
            link,
            data,
            enviada,
            comissao,
            vendas,
            avaliacao,
            imagem,
            plataforma,
            url_original,
            item_id
        )
        VALUES (?, ?, ?, ?, ?, ?, 0, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            nome,
            None,
            preco,
            desconto,
            link,
            data,
            comissao,
            vendas,
            avaliacao,
            imagem,
            plataforma,
            url_original,
            item_id
        )
    )

    conexao.commit()
    conexao.close()

    print("🆕 Produto novo adicionado ao banco!")

    return "novo"


def adicionar_oferta(
    produto,
    preco_antigo,
    preco_novo,
    desconto,
    link,
    data
):
    """
    Função antiga mantida para compatibilidade
    com partes anteriores do Radar.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id FROM ofertas WHERE link = ?",
        (link,)
    )

    oferta_existente = cursor.fetchone()

    if oferta_existente:
        print("Oferta já existe. Ignorando...")
        conexao.close()
        return False

    cursor.execute("""
        INSERT INTO ofertas (
            produto,
            preco_antigo,
            preco_novo,
            desconto,
            link,
            data
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        produto,
        preco_antigo,
        preco_novo,
        desconto,
        link,
        data
    ))

    conexao.commit()
    conexao.close()

    print("Oferta adicionada com sucesso!")

    return True


def listar_ofertas():
    criar_tabela()

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM ofertas
        ORDER BY id DESC
    """)

    ofertas = cursor.fetchall()

    conexao.close()

    return ofertas


def buscar_ofertas_nao_enviadas():
    criar_tabela()

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            produto,
            preco_antigo,
            preco_novo,
            desconto,
            link,
            comissao,
            vendas,
            avaliacao,
            imagem,
            plataforma,
            url_original
        FROM ofertas
        WHERE desconto >= 30
        AND enviada = 0
        ORDER BY desconto DESC
    """)

    ofertas = cursor.fetchall()

    conexao.close()

    return ofertas


def marcar_como_enviada(oferta_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE ofertas
        SET enviada = 1
        WHERE id = ?
        """,
        (oferta_id,)
    )

    conexao.commit()
    conexao.close()


if __name__ == "__main__":
    criar_tabela()