#!/usr/bin/env python3
import os
import sys
import psycopg2

def main():
    db_name = os.getenv("POSTGRES_DB", "datamart")
    db_user = os.getenv("POSTGRES_USER", "datamart_user")
    db_pass = os.getenv("POSTGRES_PASSWORD", "datamart_pass")
    db_host = os.getenv("POSTGRES_HOST", "db")
    db_port = os.getenv("POSTGRES_PORT", "5432")

    resultado_file = "/app/data/output/resultado/part-00000"
    if len(sys.argv) > 1:
        resultado_file = sys.argv[1]

    if not os.path.exists(resultado_file):
        print(f"Error: El archivo {resultado_file} no existe.")
        sys.exit(1)

    conn = psycopg2.connect(
        dbname=db_name, user=db_user, password=db_pass, host=db_host, port=db_port
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resultados_ventas (
            id SERIAL PRIMARY KEY,
            metodo_pago VARCHAR(50) NOT NULL,
            dia_semana VARCHAR(20) NOT NULL,
            unidades_vendidas BIGINT NOT NULL,
            UNIQUE(metodo_pago, dia_semana)
        );
    """)

    with open(resultado_file, "r") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) == 3:
                metodo, dia, unidades = parts[0], parts[1], int(parts[2])
                cursor.execute("""
                    INSERT INTO resultados_ventas (metodo_pago, dia_semana, unidades_vendidas)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (metodo_pago, dia_semana) 
                    DO UPDATE SET unidades_vendidas = EXCLUDED.unidades_vendidas;
                """, (metodo, dia, unidades))

    conn.commit()
    cursor.close()
    conn.close()
    print("Resultados cargados exitosamente en PostgreSQL.")

if __name__ == "__main__":
    main()