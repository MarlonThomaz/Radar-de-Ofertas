import re
import unicodedata


# ==========================================================
# PALAVRAS COMERCIAIS
# ==========================================================

PALAVRAS_COMERCIAIS = {
    "novo",
    "nova",
    "original",
    "oficial",
    "oferta",
    "promocao",
    "promocional",
    "qualidade",
    "alta",
    "envio",
    "imediato",
    "imperdivel",
    "melhor",
    "preco",
    "barato",
    "barata",
    "super",
    "top",
}


# ==========================================================
# NORMALIZAÇÃO
# ==========================================================

def normalizar_nome(nome):

    nome = str(nome or "").lower()

    nome = unicodedata.normalize(
        "NFD",
        nome
    )

    nome = "".join(
        caractere
        for caractere in nome
        if unicodedata.category(caractere) != "Mn"
    )

    nome = re.sub(
        r"[^a-z0-9\s]",
        " ",
        nome
    )

    nome = re.sub(
        r"\s+",
        " ",
        nome
    ).strip()

    return nome


def nome_limpo(nome):

    palavras = normalizar_nome(nome).split()

    palavras = [
        palavra
        for palavra in palavras
        if palavra not in PALAVRAS_COMERCIAIS
    ]

    return " ".join(palavras)


# ==========================================================
# MODELOS
# ==========================================================

def extrair_modelos(nome):

    nome = normalizar_nome(nome)

    modelos = set()

    # H109-3
    # HB16-2
    encontrados = re.findall(
        r"\b[a-z]{1,10}-\d{2,8}[a-z0-9]*\b",
        nome
    )

    modelos.update(encontrados)

    # D20
    # D28
    # TK12
    # BS1202
    encontrados = re.findall(
        r"\b[a-z]{2,10}\d{2,8}[a-z0-9]*\b",
        nome
    )

    modelos.update(encontrados)

    return modelos


# ==========================================================
# CAPACIDADES
# ==========================================================

def extrair_capacidades(nome):

    nome = normalizar_nome(nome)

    capacidades = set()

    # 5000mAh
    encontrados = re.findall(
        r"\b\d{3,7}\s*m\s*a\s*h\b",
        nome
    )

    for valor in encontrados:

        valor = valor.replace(" ", "")

        capacidades.add(
            valor
        )

    return capacidades


# ==========================================================
# VOLUME
# ==========================================================

def extrair_volumes(nome):

    nome = normalizar_nome(nome)

    volumes = set()

    encontrados = re.findall(
        r"\b\d+(?:[.,]\d+)?\s*(?:ml|l)\b",
        nome
    )

    for valor in encontrados:

        valor = valor.replace(",", ".")
        valor = valor.replace(" ", "")

        volumes.add(
            valor
        )

    return volumes


# ==========================================================
# PESO
# ==========================================================

def extrair_pesos(nome):

    nome = normalizar_nome(nome)

    pesos = set()

    encontrados = re.findall(
        r"\b\d+(?:[.,]\d+)?\s*(?:mg|g|kg)\b",
        nome
    )

    for valor in encontrados:

        valor = valor.replace(",", ".")
        valor = valor.replace(" ", "")

        pesos.add(
            valor
        )

    return pesos


# ==========================================================
# POTÊNCIA
# ==========================================================

def extrair_potencias(nome):

    nome = normalizar_nome(nome)

    potencias = set()

    encontrados = re.findall(
        r"\b\d+(?:[.,]\d+)?\s*w\b",
        nome
    )

    for valor in encontrados:

        valor = valor.replace(",", ".")
        valor = valor.replace(" ", "")

        potencias.add(
            valor
        )

    return potencias


# ==========================================================
# VOLTAGEM
# ==========================================================

def extrair_voltagens(nome):

    nome = normalizar_nome(nome)

    voltagens = set()

    if re.search(
        r"\b110\s*v\b",
        nome
    ):
        voltagens.add("110v")

    if re.search(
        r"\b127\s*v\b",
        nome
    ):
        voltagens.add("127v")

    if re.search(
        r"\b220\s*v\b",
        nome
    ):
        voltagens.add("220v")

    if re.search(
        r"\b240\s*v\b",
        nome
    ):
        voltagens.add("240v")

    if re.search(
        r"\bbivolt\b",
        nome
    ):
        voltagens.add("bivolt")

    return voltagens


# ==========================================================
# KITS / QUANTIDADE
# ==========================================================

def extrair_kits(nome):

    nome = normalizar_nome(nome)

    kits = set()

    # Kit 5
    encontrados = re.findall(
        r"\bkit\s*(\d+)\b",
        nome
    )

    kits.update(encontrados)

    # 5 unidades
    encontrados = re.findall(
        r"\b(\d+)\s+(?:cabos?|pecas?|unidades?|unid|un)\b",
        nome
    )

    kits.update(encontrados)

    # 10 pares
    encontrados = re.findall(
        r"\b(\d+)\s+(?:pares?|kits?)\b",
        nome
    )

    kits.update(encontrados)

    return kits


# ==========================================================
# COMPRIMENTO
# ==========================================================

def extrair_comprimentos(nome):

    nome = normalizar_nome(nome)

    comprimentos = set()

    encontrados = re.findall(
        r"\b\d+(?:[.,]\d+)?\s*(?:cm|m)\b",
        nome
    )

    for valor in encontrados:

        valor = valor.replace(",", ".")
        valor = valor.replace(" ", "")

        comprimentos.add(
            valor
        )

    return comprimentos


# ==========================================================
# DIMENSÕES EM MILÍMETROS
# ==========================================================

def extrair_tamanhos_mm(nome):

    nome = normalizar_nome(nome)

    tamanhos = set()

    encontrados = re.findall(
        r"\b\d+(?:[.,]\d+)?\s*mm\b",
        nome
    )

    for valor in encontrados:

        valor = valor.replace(",", ".")
        valor = valor.replace(" ", "")

        tamanhos.add(
            valor
        )

    return tamanhos


# ==========================================================
# MEMÓRIA / ARMAZENAMENTO
# ==========================================================

def extrair_memorias(nome):

    nome = normalizar_nome(nome)

    memorias = set()

    encontrados = re.findall(
        r"\b\d+(?:[.,]\d+)?\s*(?:gb|tb)\b",
        nome
    )

    for valor in encontrados:

        valor = valor.replace(",", ".")
        valor = valor.replace(" ", "")

        memorias.add(
            valor
        )

    return memorias


# ==========================================================
# CONECTORES
# ==========================================================

def extrair_conectores(nome):

    nome = normalizar_nome(nome)

    conectores = set()

    grupos = {

        "usb-c": [
            "usb c",
            "type c",
            "tipo c",
            "typec"
        ],

        "lightning": [
            "lightning"
        ],

        "micro-usb": [
            "micro usb",
            "microusb"
        ],

        "mini-usb": [
            "mini usb",
            "miniusb"
        ],

        "v8": [
            "v8"
        ]
    }

    for conector, palavras in grupos.items():

        for palavra in palavras:

            if palavra in nome:

                conectores.add(
                    conector
                )

                break

    return conectores


# ==========================================================
# TAMANHOS DE ROUPA / CALÇADO
# ==========================================================

def extrair_tamanhos(nome):

    nome = normalizar_nome(nome)

    tamanhos = set()

    # P, M, G, GG etc.
    encontrados = re.findall(
        r"\b(?:tamanho\s*)?(pp|p|m|g|gg|xg|xxg)\b",
        nome
    )

    tamanhos.update(
        encontrados
    )

    # Números de calçado / roupas
    encontrados = re.findall(
        r"\b(?:tamanho\s*)?(\d{2})\b",
        nome
    )

    for valor in encontrados:

        numero = int(valor)

        if 20 <= numero <= 60:

            tamanhos.add(
                valor
            )

    return tamanhos


# ==========================================================
# CORES
# ==========================================================

def extrair_cores(nome):

    nome = normalizar_nome(nome)

    cores = set()

    cores_conhecidas = {
        "preto",
        "preta",
        "branco",
        "branca",
        "vermelho",
        "vermelha",
        "azul",
        "verde",
        "amarelo",
        "amarela",
        "rosa",
        "roxo",
        "roxa",
        "lilas",
        "cinza",
        "cinza",
        "grafite",
        "prata",
        "dourado",
        "dourada",
        "marrom",
        "bege",
        "laranja",
        "transparente"
    }

    palavras = set(
        nome.split()
    )

    for cor in cores_conhecidas:

        if cor in palavras:

            cores.add(
                cor
            )

    return cores


# ==========================================================
# GÊNERO / IDADE / VARIANTES
# ==========================================================

def extrair_variantes(nome):

    nome = normalizar_nome(nome)

    variantes = set()

    grupos = {

        "masculino": [
            "men",
            "masculino",
            "homem",
            "male"
        ],

        "feminino": [
            "women",
            "feminino",
            "mulher",
            "female"
        ],

        "infantil": [
            "infantil",
            "crianca",
            "criancas",
            "kids",
            "kid",
            "child"
        ],

        "adulto": [
            "adulto",
            "adultos",
            "adult",
            "adults"
        ],

        "mini": [
            "mini"
        ],

        "max": [
            "max"
        ],

        "pro": [
            "pro"
        ],

        "ultra": [
            "ultra"
        ],

        "plus": [
            "plus"
        ],

        "lite": [
            "lite"
        ],

        "se": [
            "se"
        ],

        "standard": [
            "standard"
        ],

        "premium": [
            "premium"
        ],

        "classic": [
            "classic"
        ]
    }

    for variante, palavras in grupos.items():

        for palavra in palavras:

            padrao = rf"\b{re.escape(palavra)}\b"

            if re.search(
                padrao,
                nome
            ):

                variantes.add(
                    variante
                )

                break

    return variantes


# ==========================================================
# MATERIAIS
# ==========================================================

def extrair_materiais(nome):

    nome = normalizar_nome(nome)

    materiais = set()

    materiais_conhecidos = {
        "aco",
        "inox",
        "plastico",
        "aluminio",
        "madeira",
        "vidro",
        "silicone",
        "borracha",
        "couro",
        "metal",
        "ceramica",
        "tecido",
        "algodao",
        "nylon"
    }

    palavras = set(
        nome.split()
    )

    for material in materiais_conhecidos:

        if material in palavras:

            materiais.add(
                material
            )

    return materiais


# ==========================================================
# FRAGRÂNCIAS / SABORES
# ==========================================================

def extrair_opcoes_consumiveis(nome):

    nome = normalizar_nome(nome)

    opcoes = set()

    valores = {
        "morango",
        "chocolate",
        "baunilha",
        "cafe",
        "menta",
        "mentol",
        "lavanda",
        "citronela",
        "coco",
        "uva",
        "limao",
        "laranja",
        "melancia",
        "manga",
        "frutas"
    }

    palavras = set(
        nome.split()
    )

    for valor in valores:

        if valor in palavras:

            opcoes.add(
                valor
            )

    return opcoes


# ==========================================================
# COMPATIBILIDADE
# ==========================================================

def extrair_compatibilidades(nome):

    nome = normalizar_nome(nome)

    compatibilidades = set()

    marcas = {
        "iphone",
        "ipad",
        "samsung",
        "xiaomi",
        "redmi",
        "motorola",
        "apple",
        "android",
        "windows",
        "ps4",
        "ps5",
        "xbox",
        "nintendo"
    }

    palavras = set(
        nome.split()
    )

    for marca in marcas:

        if marca in palavras:

            compatibilidades.add(
                marca
            )

    return compatibilidades


# ==========================================================
# CARACTERÍSTICAS
# ==========================================================

def extrair_caracteristicas(nome):

    return {

        "modelos": extrair_modelos(nome),

        "capacidades": extrair_capacidades(nome),

        "volumes": extrair_volumes(nome),

        "pesos": extrair_pesos(nome),

        "potencias": extrair_potencias(nome),

        "voltagens": extrair_voltagens(nome),

        "kits": extrair_kits(nome),

        "comprimentos": extrair_comprimentos(nome),

        "tamanhos_mm": extrair_tamanhos_mm(nome),

        "memorias": extrair_memorias(nome),

        "conectores": extrair_conectores(nome),

        "tamanhos": extrair_tamanhos(nome),

        "cores": extrair_cores(nome),

        "variantes": extrair_variantes(nome),

        "materiais": extrair_materiais(nome),

        "opcoes_consumiveis": extrair_opcoes_consumiveis(nome),

        "compatibilidades": extrair_compatibilidades(nome)
    }


# ==========================================================
# CONFLITO DE QUANTIDADE
# ==========================================================

def quantidade_conflitante(a, b):

    kits_a = a["kits"]
    kits_b = b["kits"]

    if not kits_a and not kits_b:
        return False

    if bool(kits_a) != bool(kits_b):
        return True

    return kits_a.isdisjoint(
        kits_b
    )


# ==========================================================
# CONFLITO GENÉRICO
# ==========================================================

def caracteristica_conflitante(
    a,
    b,
    campo
):

    valores_a = a[campo]
    valores_b = b[campo]

    if not valores_a or not valores_b:
        return False

    return valores_a.isdisjoint(
        valores_b
    )


# ==========================================================
# CONFLITO DE VARIANTES
# ==========================================================

def variantes_conflitantes(a, b):

    variantes_a = a["variantes"]
    variantes_b = b["variantes"]

    if not variantes_a or not variantes_b:
        return False

    # ------------------------------------------------------
    # GÊNERO
    # ------------------------------------------------------

    generos_a = variantes_a & {
        "masculino",
        "feminino"
    }

    generos_b = variantes_b & {
        "masculino",
        "feminino"
    }

    if generos_a and generos_b:

        if generos_a.isdisjoint(
            generos_b
        ):
            return True

    # ------------------------------------------------------
    # IDADE
    # ------------------------------------------------------

    idade_a = variantes_a & {
        "infantil",
        "adulto"
    }

    idade_b = variantes_b & {
        "infantil",
        "adulto"
    }

    if idade_a and idade_b:

        if idade_a.isdisjoint(
            idade_b
        ):
            return True

    # ------------------------------------------------------
    # OUTRAS VARIANTES
    # ------------------------------------------------------

    outras_a = variantes_a - {
        "masculino",
        "feminino",
        "infantil",
        "adulto"
    }

    outras_b = variantes_b - {
        "masculino",
        "feminino",
        "infantil",
        "adulto"
    }

    if outras_a and outras_b:

        if outras_a.isdisjoint(
            outras_b
        ):
            return True

    return False


# ==========================================================
# CONFLITO DE VOLTAGEM
# ==========================================================

def voltagem_conflitante(a, b):

    voltagens_a = a["voltagens"]
    voltagens_b = b["voltagens"]

    if not voltagens_a or not voltagens_b:
        return False

    # Se forem explicitamente diferentes,
    # tratamos como produtos diferentes.
    if voltagens_a.isdisjoint(
        voltagens_b
    ):
        return True

    return False


# ==========================================================
# TODOS OS CONFLITOS
# ==========================================================

def existe_conflito(a, b):

    # Quantidade / kit
    if quantidade_conflitante(a, b):
        return True

    # Capacidade
    if caracteristica_conflitante(
        a,
        b,
        "capacidades"
    ):
        return True

    # Volume
    if caracteristica_conflitante(
        a,
        b,
        "volumes"
    ):
        return True

    # Peso
    if caracteristica_conflitante(
        a,
        b,
        "pesos"
    ):
        return True

    # Voltagem
    if voltagem_conflitante(
        a,
        b
    ):
        return True

    # Comprimento
    if caracteristica_conflitante(
        a,
        b,
        "comprimentos"
    ):
        return True

    # Tamanho em mm
    if caracteristica_conflitante(
        a,
        b,
        "tamanhos_mm"
    ):
        return True

    # Memória / armazenamento
    if caracteristica_conflitante(
        a,
        b,
        "memorias"
    ):
        return True

    # Conector
    if caracteristica_conflitante(
        a,
        b,
        "conectores"
    ):
        return True

    # Tamanho
    if caracteristica_conflitante(
        a,
        b,
        "tamanhos"
    ):
        return True

    # Cor
    if caracteristica_conflitante(
        a,
        b,
        "cores"
    ):
        return True

    # Material
    if caracteristica_conflitante(
        a,
        b,
        "materiais"
    ):
        return True

    # Sabor / fragrância
    if caracteristica_conflitante(
        a,
        b,
        "opcoes_consumiveis"
    ):
        return True

    # Compatibilidade
    if caracteristica_conflitante(
        a,
        b,
        "compatibilidades"
    ):
        return True

    # Variantes
    if variantes_conflitantes(
        a,
        b
    ):
        return True

    # ======================================================
    # POTÊNCIA
    # ======================================================
    #
    # NÃO é conflito automático.
    #
    # 120W
    # 120W + 67W
    # 120W + 67W + 33W
    #
    # podem representar o mesmo produto.
    #
    # ======================================================

    return False


# ==========================================================
# MESMO MODELO
# ==========================================================

def mesmo_modelo(a, b):

    modelos_a = a["modelos"]
    modelos_b = b["modelos"]

    if not modelos_a or not modelos_b:
        return False

    return not modelos_a.isdisjoint(
        modelos_b
    )


# ==========================================================
# NOME IGUAL
# ==========================================================

def nomes_iguais(nome_a, nome_b):

    return (
        nome_limpo(nome_a)
        ==
        nome_limpo(nome_b)
    )


# ==========================================================
# SEMELHANÇA
# ==========================================================

def calcular_semelhanca(
    nome_a,
    nome_b
):

    palavras_a = set(
        nome_limpo(nome_a).split()
    )

    palavras_b = set(
        nome_limpo(nome_b).split()
    )

    if not palavras_a or not palavras_b:
        return 0

    intersecao = (
        palavras_a &
        palavras_b
    )

    menor = min(
        len(palavras_a),
        len(palavras_b)
    )

    return (
        len(intersecao) /
        menor
    )


# ==========================================================
# DUPLICATA SEMÂNTICA
# ==========================================================

def sao_semelhantes(
    produto_a,
    produto_b
):

    nome_a = produto_a.get(
        "nome",
        ""
    )

    nome_b = produto_b.get(
        "nome",
        ""
    )

    caracteristicas_a = (
        extrair_caracteristicas(
            nome_a
        )
    )

    caracteristicas_b = (
        extrair_caracteristicas(
            nome_b
        )
    )

    # ======================================================
    # PRIMEIRA BARREIRA
    # ======================================================

    if existe_conflito(
        caracteristicas_a,
        caracteristicas_b
    ):
        return False

    # ======================================================
    # REGRA 1
    # ======================================================

    # Título essencialmente igual.
    if nomes_iguais(
        nome_a,
        nome_b
    ):
        return True

    # ======================================================
    # REGRA 2
    # ======================================================

    # Mesmo modelo + título muito semelhante.
    if mesmo_modelo(
        caracteristicas_a,
        caracteristicas_b
    ):

        semelhanca = (
            calcular_semelhanca(
                nome_a,
                nome_b
            )
        )

        if semelhanca >= 0.90:
            return True

    # ======================================================
    # REGRA 3
    # ======================================================

    # Sem modelo explícito:
    # exigimos semelhança extremamente alta.
    if (
        not caracteristicas_a["modelos"]
        and
        not caracteristicas_b["modelos"]
    ):

        semelhanca = (
            calcular_semelhanca(
                nome_a,
                nome_b
            )
        )

        if semelhanca >= 0.98:
            return True

    return False


# ==========================================================
# REMOÇÃO
# ==========================================================

def remover_duplicados_semanticos(
    produtos
):

    produtos_mantidos = []

    for produto in produtos:

        duplicado_de = None

        for produto_existente in produtos_mantidos:

            if sao_semelhantes(
                produto,
                produto_existente
            ):

                duplicado_de = (
                    produto_existente
                )

                break

        if duplicado_de:

            print(
                "\n🔎 DUPLICATA ENCONTRADA:"
            )

            print(
                f"❌ {produto.get('nome', '')}"
            )

            print(
                "↳ semelhante a:"
            )

            print(
                f"✅ {duplicado_de.get('nome', '')}"
            )

            continue

        produtos_mantidos.append(
            produto
        )

    return produtos_mantidos