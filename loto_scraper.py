# loto_scraper.py

import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def obtener_resultados_loto():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    resultados = []

    try:
        driver = webdriver.Chrome(options=options)
        driver.get("https://loto.com.ni/diaria/")
        time.sleep(2)

        pagina_actual = 1
        while pagina_actual <= 10:
            print(f"\n📄 Procesando página {pagina_actual}...")
            soup = BeautifulSoup(driver.page_source, "html.parser")
            bloques_resultados = soup.select("div.Rtable.Rtable--2cols.Rtable--collapse")

            for bloque in bloques_resultados:
                encabezado = bloque.select_one("div.Rtable-cell--head")
                if not encabezado:
                    continue

                spans = encabezado.find_all("span")
                fecha = spans[0].text.strip() if len(spans) > 0 else ""
                hora = spans[1].text.strip() if len(spans) > 1 else ""
                sorteo = spans[2].text.strip() if len(spans) > 2 else ""

                bolas = bloque.select("div.esferas.esfera-amarillo span")
                numeros = [b.text.strip() for b in bolas]
                pares = [numeros[i] + numeros[i + 1] for i in range(0, len(numeros) - 1, 2)]

                print(f"\n📅 Fecha: {fecha}")
                print(f"🕘 Hora: {hora}")
                print(f"🎟️ Sorteo: {sorteo}")
                print("🎯 Números ganadores:")
                for par in pares:
                    print(f"🎱 {par}")

                resultados.append({
                    "fecha": fecha,
                    "hora": hora,
                    "sorteo": sorteo,
                    "pares": ', '.join(pares)
                })

            # Cambiar de página
            try:
                boton_siguiente = driver.find_element(By.CLASS_NAME, 'btn_next')
                if boton_siguiente.is_displayed():
                    boton_siguiente.click()
                    pagina_actual += 1
                    time.sleep(5)
                else:
                    print("🚫 Botón siguiente no visible, finalizando...")
                    break
            except Exception as e:
                print("⚠️ No se pudo avanzar a la siguiente página:", e)
                break

    except Exception as e:
        print("❌ Error general:", e)

    finally:
        driver.quit()

    # Guardar CSV
    with open("resultados_loto.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["fecha", "hora", "sorteo", "pares"])
        writer.writeheader()
        writer.writerows(resultados)

    print(f"\n✅ Se guardaron {len(resultados)} resultados en 'resultados_loto.csv'")
