import os
import requests
import time

# --- CONFIGURACIÓN DESDE SECRETS (Invisibles) ---
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

SKIN_NAME = "M4A1-S | Liquidation (Factory New)"
PRECIO_MAXIMO = 15.75

def consultar():
    # URL de la M4A1-S Liquidación FN
    url = "https://steamcommunity.com/market/listings/730/M4A1-S%20%7C%20Liquidation%20%28Factory%20New%29/render/?query=&start=0&count=10&currency=1&language=english"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Referer': 'https://steamcommunity.com/market/listings/730/M4A1-S%20%7C%20Liquidation%20%28Factory%20New%29'
        }
        
        res = requests.get(url, headers=headers, timeout=15)
        data = res.json()

        if not data or data.get("total_count", 0) == 0:
            print(f"[{time.strftime('%H:%M:%S')}] Steam no devolvió datos.")
            return False

        for listing_id in data["listinginfo"]:
            listing = data["listinginfo"][listing_id]
            # Cálculo de precio con comisión de Steam incluida
            precio = (listing["converted_price"] + listing["converted_fee"]) / 100
            
            print(f"[{time.strftime('%H:%M:%S')}] Precio actual encontrado: ${precio:.2f}")

            if precio < PRECIO_MAXIMO:
                msg = f"🚨 ¡OFERTA! | Precio: ${precio:.2f} | Link: https://steamcommunity.com/market/listings/730/M4A1-S%20%7C%20Liquidation%20(Factory%20New)"
                requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
                print(f">>> ALERTA ENVIADA A TELEGRAM: ${precio:.2f}")
                return True # Terminamos si encontramos una oferta
        
        return False
                
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Error: {e}")
    return False

# --- EJECUCIÓN ÚNICA ---
print("==========================================")
print(f" Buscando: {SKIN_NAME} < ${PRECIO_MAXIMO}")
print("==========================================")

# Ejecuta la consulta una sola vez (GitHub se encarga de la repetición)
consultar()
