import requests
import time

# --- CONFIGURACIÓN ---
TOKEN = "1139831374:AAF-idyHp4e0F3fuba3LrOkpkPC3CuloI-M"
CHAT_ID = "99216389"
SKIN_NAME = "M4A1-S | Liquidation (Factory New)"
PRECIO_MAXIMO = 15.75  # <--- Nuevo objetivo

def consultar():
    url = "https://steamcommunity.com/market/listings/730/M4A1-S%20%7C%20Liquidation%20%28Factory%20New%29/render/?query=&start=0&count=10&currency=1&language=english"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Referer': 'https://steamcommunity.com/market/listings/730/M4A1-S%20%7C%20Liquidation%20%28Factory%20New%29'
        }
        
        res = requests.get(url, headers=headers, timeout=15)
        data = res.json()

        if data.get("total_count", 0) == 0:
            print(f"[{time.strftime('%H:%M:%S')}] Steam no devolvió datos. (IP en espera)")
            return False

        encontrado = False
        for listing_id in data["listinginfo"]:
            listing = data["listinginfo"][listing_id]
            precio = (listing["converted_price"] + listing["converted_fee"]) / 100
            
            print(f"[{time.strftime('%H:%M:%S')}] Precio actual: ${precio:.2f}")

            if precio < PRECIO_MAXIMO:
                msg = f"🚨 ¡OFERTA! | Precio: ${precio:.2f} | Link: https://steamcommunity.com/market/listings/730/M4A1-S%20%7C%20Liquidation%20(Factory%20New)"
                requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
                print(f">>> ALERTA ENVIADA: ${precio:.2f}")
                encontrado = True
        
        return encontrado
                
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Error: {e}")
    return False

print("==========================================")
print("       MONITOR DE PRECIOS ACTIVADO")
print(f" Buscando: {SKIN_NAME} < ${PRECIO_MAXIMO}")
print("==========================================\n")

# Aviso de reinicio en Telegram
requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=🚀 Monitor actualizado. Objetivo: ${PRECIO_MAXIMO}")

while True:
    consultar()
    print(f"\n[{time.strftime('%H:%M:%S')}] Esperando 10 minutos para el próximo chequeo...")
    time.sleep(600)