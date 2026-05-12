import os
import requests
import time

# --- CONFIGURACIÓN ---
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
PRECIO_MAXIMO = 4000.0

# URLs
URL_COTO = "https://www.cotodigital.com.ar/sitios/cdigi/productos/-vino-syrah-cabernet-callia-esperado-750ml/_/R-00572882-00572882-200"
URL_MASONLINE = "https://www.masonline.com.ar/vino-tinto-esperado-syrah-malbec-750ml-2/p"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def consultar_coto():
    try:
        res = requests.get(URL_COTO, headers=headers, timeout=20)
        texto = res.text
        if "atg_store_newPrice" in texto:
            parte_precio = texto.split('atg_store_newPrice')[1].split('>')[1].split('<')[0]
            precio_limpio = parte_precio.replace('$', '').replace('.', '').replace(',', '.').strip()
            return float(precio_limpio)
    except:
        return None

def consultar_masonline():
    try:
        res = requests.get(URL_MASONLINE, headers=headers, timeout=20)
        texto = res.text
        # MasOnline suele guardar el precio en un JSON interno o etiqueta de precio
        # Buscamos el patrón común de precio en su HTML
        if '"price":' in texto:
            parte_precio = texto.split('"price":')[1].split(',')[0]
            return float(parte_precio)
    except:
        return None

# --- EJECUCIÓN ---
precio_coto = consultar_coto()
precio_mas = consultar_masonline()

# Log en GitHub
print(f"[{time.strftime('%H:%M:%S')}] Coto: ${precio_coto if precio_coto else 'Error'}")
print(f"[{time.strftime('%H:%M:%S')}] MasOnline: ${precio_mas if precio_mas else 'Error'}")

# Alerta Coto
if precio_coto and precio_coto < PRECIO_MAXIMO:
    msg = f"🍷 ¡OFERTA COTO! | Callia Esperado: ${precio_coto} | Link: {URL_COTO}"
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")

# Alerta MasOnline
if precio_mas and precio_mas < PRECIO_MAXIMO:
    msg = f"🍷 ¡OFERTA MAS ONLINE! | Callia Esperado: ${precio_mas} | Link: {URL_MASONLINE}"
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
