#!/usr/bin/env python3
import sys
import time
import csv
from datetime import datetime

DIAS = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 secuencial.py <ruta_al_csv>")
        sys.exit(1)

    archivo = sys.argv[1]
    start_time = time.time()

    resultados = {}

    with open(archivo, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)

        for row in reader:
            if len(row) < 8:
                continue
            try:
                fecha_str = row[1]
                cantidad = int(row[5])
                metodo_pago = row[7].strip()

                dt = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
                dia_semana = DIAS[dt.weekday()]

                key = (metodo_pago, dia_semana)
                resultados[key] = resultados.get(key, 0) + cantidad
            except (ValueError, IndexError):
                continue

    end_time = time.time()

    print("--- RESULTADOS SECUENCIAL ---")
    for (mp, ds), total in sorted(resultados.items()):
        print(f"{mp}\t{ds}\t{total}")

    print(f"\nTiempo de ejecucion secuencial: {end_time - start_time:.4f} segundos")

if __name__ == "__main__":
    main()