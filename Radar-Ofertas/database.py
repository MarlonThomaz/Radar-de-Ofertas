import sqlite3


def criar_tabela():
    conexao = sqlite3.connect("data/ofertas.db")
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ofertas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            preco_antigo REAL,
            preco_novo REAL,
            desconto REAL,
            link TEXT,
            data TEXT
        )
    """)

    try:
        cursor.execute(
            "ALTER TABLE ofertas ADD COLUMN enviada INTEGER DEFAULT 0"
        )
    except sqlite3.OperationalError:
        pass

    conexao.commit()
    conexao.close()


def adicionar_oferta(produto, preco_antigo, preco_novo, desconto, link, data):
    conexao = sqlite3.connect("data/ofertas.db")
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id FROM ofertas WHERE link = ?",
        (link,)
    )

    oferta_existente = cursor.fetchone()

    if oferta_existente:
        print("Oferta já existe. Ignorando...")
        conexao.close()
        return

    cursor.execute("""
        INSERT INTO ofertas
        (produto, preco_antigo, preco_novo, desconto, link, data)
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


def listar_ofertas():
    conexao = sqlite3.connect("data/ofertas.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM ofertas")

    ofertas = cursor.fetchall()

    conexao.close()

    return ofertas

def buscar_ofertas_nao_enviadas():
    conexao = sqlite3.connect("data/ofertas.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, produto, preco_antigo, preco_novo, desconto, link
        FROM ofertas
        WHERE desconto >= 30
        AND enviada = 0
        ORDER BY desconto DESC
    """)

    ofertas = cursor.fetchall()

    conexao.close()

    return ofertas

def marcar_como_enviada(oferta_id):
    conexao = sqlite3.connect("data/ofertas.db")
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE ofertas SET enviada = 1 WHERE id = ?",
        (oferta_id,)
    )

    conexao.commit()
    conexao.close()



if __name__ == "__main__":
    criar_tabela()