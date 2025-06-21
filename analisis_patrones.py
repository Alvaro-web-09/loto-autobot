import pandas as pd
from collections import Counter

def analizar_patrones():
    df = pd.read_csv("resultados_loto.csv")
    df.columns = [col.strip().lower() for col in df.columns]

    df["dia_semana"] = df["fecha"].apply(lambda x: x.split()[0])
    df["hora_exacta"] = df["hora"].str.strip()
    df["numero"] = df["pares"].apply(lambda x: int(str(x).split(",")[1]) if "," in str(x) else int(x))


    # Clasifica el bloque horario
    def clasificar_bloque(dia, hora):
        if dia == "Sábado":
            if "11:00 AM" in hora:
                return "MAÑANA"
            elif "3:00 PM" in hora:
                return "TARDE"
            elif "6:00 PM" in hora:
                return "NOCHE"
            elif "9:00 PM" in hora:
                return "EXTRA NOCHE"
        else:
            if "11:00 AM" in hora:
                return "MAÑANA"
            elif "3:00 PM" in hora:
                return "TARDE"
            elif "9:00 PM" in hora:
                return "NOCHE"
        return "OTRO"

    df["bloque"] = df.apply(lambda row: clasificar_bloque(row["dia_semana"], row["hora"]), axis=1)

    print("📊 Análisis de patrones\n")

    # Frecuencia total
    print("🔢 Frecuencia total de números:")
    total = Counter(df["numero"])
    for num, count in total.most_common(10):
        print(f"🎱 Número {num}: {count} veces")

    # Por día de la semana
    print("\n📅 Frecuencia por día de la semana:")
    for dia in df["dia_semana"].unique():
        subset = df[df["dia_semana"] == dia]
        conteo = Counter(subset["numero"])
        print(f"\n📆 {dia}")
        for num, count in conteo.most_common(5):
            print(f"🎯 {num} ({count} veces)")

    # Por bloque
    print("\n🕒 Frecuencia por bloque horario:")
    for bloque in df["bloque"].unique():
        subset = df[df["bloque"] == bloque]
        conteo = Counter(subset["numero"])
        print(f"\n⏰ {bloque}")
        for num, count in conteo.most_common(5):
            print(f"🎲 {num} ({count} veces)")

    # 🔍 Por hora exacta
    print("\n⏱️ Frecuencia por hora exacta:")
    for hora in sorted(df["hora_exacta"].unique()):
        subset = df[df["hora_exacta"] == hora]
        conteo = Counter(subset["numero"])
        print(f"\n🕘 {hora}")
        for num, count in conteo.most_common(5):
            print(f"🎯 {num} ({count} veces)")
