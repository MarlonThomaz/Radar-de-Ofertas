from playwright.sync_api import sync_playwright
import time

GRUPO = "https://chat.whatsapp.com/EAW573DlsraFyIuBjL36qM"


def enviar_oferta(mensagem):
    print("\n📱 ABRINDO WHATSAPP...")

    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=False)

        pagina = navegador.new_page()

        pagina.goto("https://web.whatsapp.com")

        print("\n📱 Escaneie o QR Code do WhatsApp Web.")
        print("Depois que o WhatsApp carregar, o script continuará automaticamente.")

        pagina.wait_for_timeout(30000)

        print("\n🔎 Abrindo grupo...")

        pagina.goto(GRUPO)

        pagina.wait_for_timeout(10000)

        print("\n📝 Preparando mensagem...")

        pagina.keyboard.type(mensagem)

        pagina.keyboard.press("Enter")

        print("\n✅ Mensagem enviada!")

        time.sleep(5)

        navegador.close()

    return True