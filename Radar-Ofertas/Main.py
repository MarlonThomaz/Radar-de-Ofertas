from database import (
    criar_tabela,
    buscar_ofertas_nao_enviadas,
    marcar_como_enviada
)

from scraper import analisar_ofertas
from mensagem import criar_mensagem
from enviador import enviar_oferta


print("🚀 Radar de Ofertas iniciando...")

criar_tabela()

analisar_ofertas()

ofertas = buscar_ofertas_nao_enviadas()

print("\n--- OFERTAS NOVAS ---")

for oferta in ofertas:

    oferta_id = oferta[0]

    dados_oferta = oferta[1:]

    mensagem = criar_mensagem(dados_oferta)

    enviado = enviar_oferta(mensagem)

    if enviado:
        marcar_como_enviada(oferta_id)
        print("✅ Oferta marcada como enviada!")
    else:
        print("❌ Falha no envio. Oferta continua pendente!")


print("\n✅ Radar finalizado!")