import pandas as pd
from collections import defaultdict, Counter
from datetime import datetime

def clasificar_bloque(hora_str):
    """Clasifica la hora en bloques horarios."""
    if "PM" in hora_str:
        if "9:00" in hora_str:
            return "NOCHE"
        elif "3:00" in hora_str:
            return "TARDE"
    elif "AM" in hora_str and "11:00" in hora_str:
        return "MAÑANA"
    return "OTRO"  # Horarios no clasificados

def predecir_numeros():
    try:
        # Cargar CSV
        df = pd.read_csv("resultados_loto.csv")

        # Limpiar y extraer datos
        df['fecha'] = df['fecha'].str.replace('"', '').str.strip()
        df['bloque'] = df['hora'].apply(clasificar_bloque)

        # Extraer solo el número del campo 'pares'
        df['numero'] = df['pares'].astype(str).str.extract(r'(\d+)').astype(int)

        # Agrupar por bloque horario
        historial = defaultdict(list)
        for _, fila in df.iterrows():
            historial[fila['bloque']].append(fila['numero'])

        print(f"\n🎯 Predicción basada en historial:")
        print(f"📅 Basado en el historial hasta: {df['fecha'].iloc[0]}")
        print(f"📆 Predicción para el próximo sorteo: sábado 21 de junio, 2025\n")

        for bloque, numeros in historial.items():
            contador = Counter(numeros)
            if contador:
                print(f"🕒 {bloque}")
                for numero, freq in contador.most_common(3):
                    print(f"🔮 {numero} (apareció {freq} veces)")
                print()
            else:
                print(f"🕒 {bloque}\n– Sin datos –\n")

    except Exception as e:
        print(f"🚨 Ocurrió un error inesperado: {e}")

# Ejecutar solo si se llama directamente
if __name__ == "__main__":
    predecir_numeros()
