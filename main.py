import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from flask import Flask, request

# ==========================================
# 1. CONFIGURAÇÕES INICIAIS
# ==========================================
TOKEN_BOT = "8713000127:AAGGTcj0wuKqqPzEhfhrWQuDTRWb8Dx3nDw"
SEU_ID_TELEGRAM = 7665685378
ID_GRUPO_VIP = -1004452403722

# Deixamos preenchido temporariamente para o bot iniciar sem dar erro
LINK_BANNER_BOAS_VINDAS = "AgACAgEAAxkBAAFOValqS0Lwkdjhe4pE9eioLo3Ix9rzdQAC8wtrG1MIWEbYAYELiw9weQEAAwIAA3kAAzYE"
LINK_QRCODE_PIX = "AgACAgEAAxkBAAFOVbBqS0PSwscNNP18p3ba8LnbAc1gkQAC4QtrG22QWEY81CLHVd7bzAEAAtwIAA3gAAzWE"

# Suas carteiras oficiais configuradas
CARTEIRA_BTC = "bc1qv0vt52xa356n5sfz6ayq9enfr77teemr4htqtf"
CARTEIRA_ETH = "0x68c4a8312b50D1506619314b29981Fe3731035E0"
CARTEIRA_LTC = "ltc1qpcuzhk48n0udpcv64n5x8fjapf505j2qj3ketf"
CARTEIRA_USDT = "0x1e75616b576d7f66f0cd8176ee2f70bef1fe8ddb"

bot = telebot.TeleBot(TOKEN_BOT, threaded=False)
app = Flask(__name__)

# ==========================================
# EXTRAÇÃO AUTOMÁTICA DE FILE ID (Mande as fotos para o seu bot NOVO!)
# ==========================================
@bot.message_handler(content_types=['photo'])
def receber_qualquer_foto(message):
    file_id_gerado = message.photo[-1].file_id
    texto_resposta = (
        f"📸 *Nova imagem detectada pelo seu Bot #2!*\n\n"
        f"Copie o código abaixo:\n\n"
        f"`{file_id_gerado}`"
    )
    bot.reply_to(message, texto_resposta, parse_mode="Markdown")

# --- MENSAGEM DE BOAS VINDAS DO BOT ---
@bot.message_handler(commands=['start'])
def enviar_boas_vindas(message):
    try:
        idioma_usuario = message.from_user.language_code
        markup = InlineKeyboardMarkup(row_width=1)
        
        if idioma_usuario and 'pt' in idioma_usuario:
            texto = "👋 Bem-vindo ao bot oficial!\n\nMande as fotos do Banner e do QR Code aqui no chat para descobrir os novos File IDs."
        else:
            texto = "👋 Welcome!\n\nSend the Banner and QR Code images here to discover their new File IDs."
            
        bot.send_message(message.chat.id, texto, reply_markup=markup, parse_mode="Markdown")
    except Exception as e:
        print(f"Erro no start: {e}", flush=True)

# ==========================================
# 5. ROTAS DO SERVIDOR WEB (RENDER)
# ==========================================
@app.route('/' + TOKEN_BOT, methods=['POST'])
def getMessage():
    try:
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200
    except Exception as e:
        print(f"Erro no webhook: {e}", flush=True)
        return "Erro", 500

@app.route("/")
def webhook():
    bot.remove_webhook()
    url_render = "https://two-bot3231.onrender.com" 
    bot.set_webhook(url=f"{url_render}/{TOKEN_BOT}")
    return "Webhook configurado com sucesso!", 200

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host="0.0.0.0", port=port)
