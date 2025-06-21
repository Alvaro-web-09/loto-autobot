try:
    from loto_scraper import obtener_resultados_loto as extraer_datos
    from analisis_patrones import analizar_patrones
    from predictor import predecir_numeros

    print("🔄 Obteniendo resultados...")
    extraer_datos()

    print("\n📊 Analizando patrones...")
    analizar_patrones()

    print("\n🎯 Predicción basada en historial:")
    predecir_numeros()

except ImportError as e:
    print("🚨 Error al importar módulos:", e)
except Exception as e:
    print("🚨 Ocurrió un error inesperado:", e)
