import os
import requests
import time

# --- CONFIGURACIÓN ---
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
URL_VINO = "https://www.cotodigital.com.ar/sitios/cdigi/productos/-vino-syrah-cabernet-callia-esperado-750ml/_/R-00572882-00572882-200"
PRECIO_MAXIMO = 4000.0

def consultar_coto():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        res = requests.get(URL_VINO, headers=headers, timeout=20)
        # Buscamos el precio en el texto de la página
        texto = res.text
        
        # Coto suele poner el precio en una clase llamada "atg_store_newPrice"
        if "atg_store_newPrice" in texto:
            parte_precio = texto.split('atg_store_newPrice')[1].split('>')[1].split('<')[0]
            # Limpiamos el texto para quedarnos solo con el número
            precio_limpio = parte_precio.replace('$', '').replace('.', '').replace(',', '.').strip()
            precio_final = float(precio_limpio)
            
            print(f"[{time.strftime('%H:%M:%S')}] Precio del Esperado: ${precio_final}")
            
            if precio_final < PRECIO_MAXIMO:
                msg = f"🍷 ¡OFERTA VINO ESPERADO! | Precio: ${precio_final} | Link: {URL_VINO}"
                requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
                print("Alerta enviada!")
        else:
            print("No se pudo encontrar el precio en la página. Puede que hayan cambiado el diseño.")
            
    except Exception as e:
        print(f"Error al consultar Coto: {e}")

consultar_coto()
