from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re
import datetime

# Configuramos el Chrome invisible para engañar al escudo
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36')

try:
    driver = webdriver.Chrome(options=options)
    driver.get("https://resultadosegundavuelta.onpe.gob.pe/main/resumen")
    time.sleep(10) # Esperamos 10 segundos para burlar la seguridad
    texto = driver.find_element(By.TAG_NAME, "body").text
    driver.quit()

    texto_limpio = texto.replace(',', '').replace('.', '')

    roberto_match = re.search(r'S[AÁaá]NCHEZ\D*?(\d{6,8})', texto_limpio, re.IGNORECASE)
    keiko_match = re.search(r'FUJIMORI\D*?(\d{6,8})', texto_limpio, re.IGNORECASE)

    if roberto_match and keiko_match:
        votos_roberto = int(roberto_match.group(1))
        votos_keiko = int(keiko_match.group(1))
        diferencia = abs(votos_roberto - votos_keiko)
        
        ganador = "Roberto Sánchez" if votos_roberto > votos_keiko else "Keiko Fujimori"
        color = "#d32f2f" if votos_roberto > votos_keiko else "#f57c00"
        diferencia_str = f"{diferencia:,}".replace(',', '.')
        
        # Hora actual
        hora = datetime.datetime.now() - datetime.timedelta(hours=5) # Hora Perú
        hora_str = hora.strftime("%d/%m/%Y %I:%M:%S %p")

        html = f"""
        <!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Diferencia ONPE</title>
        <style>body{{font-family:'Segoe UI', Tahoma, sans-serif;background:#f0f2f5;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;}}
        .card{{background:white;padding:40px;border-radius:20px;box-shadow:0 10px 20px rgba(0,0,0,0.1);text-align:center;max-width:400px;width:90%;}}
        h3{{color:#555;margin-bottom:5px;font-weight:normal;}}
        h1{{color:{color};font-size:55px;margin:10px 0;}}
        .ganador{{font-size:24px;font-weight:bold;color:#333;}}
        .footer{{margin-top:20px;font-size:12px;color:#999;}}</style></head>
        <body><div class="card">
        <h3>Diferencia actual de votos:</h3>
        <h1>{diferencia_str}</h1>
        <div class="ganador">A favor de:<br><span style="color:{color};">{ganador}</span></div>
        <div class="footer">🛡️ Escudo de la ONPE superado<br>Última actualización: {hora_str} (Hora Perú)</div>
        </div></body></html>
        """
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
except Exception as e:
    pass
