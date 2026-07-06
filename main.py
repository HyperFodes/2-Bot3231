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

# Deixamos temporariamente vazios para você gerar os novos oficiais enviados diretamente para ESTE bot!
LINK_BANNER_BOAS_VINDAS = "COLOQUE_O_FILE_ID_DO_BANNER_AQUI"
LINK_QRCODE_PIX = "COLOQUE_O_FILE_ID_DO_QRCODE_AQUI"

# Suas carteiras oficiais configuradas
CARTEIRA_BTC = "bc1qv0vt52xa356n5sfz6ayq9enfr77teemr4htqtf"
CARTEIRA_ETH = "0x68c4a8312b50D1506619314b29981Fe3731035E0"
CARTEIRA_LTC = "ltc1qpcuzhk48n0udpcv64n5x8fjapf505j2qj3ketf"
CARTEIRA_USDT = "0x1e75616b576d7f66f0cd8176ee2f70bef1fe8ddb"

bot = telebot.TeleBot(TOKEN_BOT, threaded=False)
app = Flask(__name__)

usuarios_comprando = {}

# ==========================================
# EXTRAÇÃO AUTOMÁTICA DE FILE ID (Mande as fotos para o bot!)
# ==========================================
@bot.message_handler(content_types=['photo'])
def receber_qualquer_foto(message):
    # Pega o File ID correto gerado por este novo bot
    file_id_gerado = message.photo[-1].file_id
    
    texto_resposta = (
        f"📸 *Nova imagem detectada pelo seu Bot #2!*\n\n"
        f"Copie o código abaixo e guarde para colocar nas variáveis:\n\n"
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
            texto = "👋 Bem-vindo ao bot oficial do Criador!\n\nGaranta seu *ACESSO VITALÍCIO* escolhendo sua forma de pagamento:"
            btn_pix = InlineKeyboardButton("🇧🇷 PIX (R$ 30,00)", callback_data="menu_pix")
            btn_stars = InlineKeyboardButton("⭐ Telegram Stars (900 Stars)", callback_data="stars_900")
            btn_crypto = InlineKeyboardButton("🪙 Crypto Dollars ($ 5.00)", callback_data="menu_crypto")
            markup.add(btn_pix, btn_stars, btn_crypto)
        else:
            texto = "👋 Welcome to the Creator's official bot!\n\nGet your *LIFETIME ACCESS* by choosing your payment method:"
            btn_stars = InlineKeyboardButton("⭐ Telegram Stars (900 Stars)", callback_data="stars_900")
            btn_crypto = InlineKeyboardButton("🪙 Crypto Dollars ($ 5.00)", callback_data="menu_crypto")
            btn_pix = InlineKeyboardButton("🇧🇷 Brazilian PIX (R$ 30,00)", callback_data="menu_pix")
            markup.add(btn_stars, btn_crypto, btn_pix)
        
        bot.send_photo(message.chat.id, LINK_BANNER_BOAS_VINDAS, caption=texto, reply_markup=markup, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Configurando File IDs... Use os códigos recebidos ao enviar imagens.\n\nTexto alternativo:\n{texto}", reply_markup=markup, parse_mode="Markdown")

# --- GERENCIAMENTO DOS BOTÕES ---
@bot.callback_query_handler(func=lambda call: True)
def escutar_botoes(call):
    chat_id =
