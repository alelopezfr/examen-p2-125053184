import os
import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="DataMart Sales API - Matricula 125053184")

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "datamart"),
        user=os.getenv("POSTGRES_USER", "datamart_user"),
        password=os.getenv("POSTGRES_PASSWORD", "datamart_pass"),
        host=os.getenv("POSTGRES_HOST", "db"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )

class ResultadoSchema(BaseModel):
    metodo_pago: str
    dia_semana: str
    unidades_vendidas: int

@app.get("/")
def home():
    return {"mensaje": "API DataMart activa. Matricula: 125053184"}

@app.get("/resultados")
def get_resultados():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, metodo_pago, dia_semana, unidades_vendidas FROM resultados_ventas;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {"id": r[0], "metodo_pago": r[1], "dia_semana": r[2], "unidades_vendidas": r[3]}
        for r in rows
    ]

@app.get("/resultados/{metodo_pago}")
def get_resultado_by_metodo(metodo_pago: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, metodo_pago, dia_semana, unidades_vendidas FROM resultados_ventas WHERE LOWER(metodo_pago) = LOWER(%s);",
        (metodo_pago,)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Metodo de pago no encontrado")

    return [
        {"id": r[0], "metodo_pago": r[1], "dia_semana": r[2], "unidades_vendidas": r[3]}
        for r in rows
    ]

@app.post("/resultados")
def create_or_update_resultado(data: ResultadoSchema):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO resultados_ventas (metodo_pago, dia_semana, unidades_vendidas)
        VALUES (%s, %s, %s)
        ON CONFLICT (metodo_pago, dia_semana)
        DO UPDATE SET unidades_vendidas = EXCLUDED.unidades_vendidas
        RETURNING id;
    """, (data.metodo_pago, data.dia_semana, data.unidades_vendidas))

    new_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": "Registro guardado correctamente", "id": new_id, "data": data}

@app.delete("/resultados/{metodo_pago}/{dia_semana}")
def delete_resultado(metodo_pago: str, dia_semana: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM resultados_ventas WHERE LOWER(metodo_pago) = LOWER(%s) AND LOWER(dia_semana) = LOWER(%s);",
        (metodo_pago, dia_semana)
    )
    deleted = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"mensaje": f"Registro ({metodo_pago}, {dia_semana}) eliminado con exito."}

@app.get("/resultados/{metodo_pago}/{dia_semana}")
def obtener_resultado_especifico(metodo_pago: str, dia_semana: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, metodo_pago, dia_semana, unidades_vendidas 
        FROM resultados_ventas 
        WHERE LOWER(metodo_pago) = LOWER(%s) AND LOWER(dia_semana) = LOWER(%s);
        """,
        (metodo_pago, dia_semana)
    )
    resultado = cur.fetchone()
    cur.close()
    conn.close()
    
    if not resultado:
        raise HTTPException(status_code=404, detail="No se encontraron registros para esta combinación")
        
    return {
        "id": resultado[0],
        "metodo_pago": resultado[1],
        "dia_semana": resultado[2],
        "unidades_vendidas": resultado[3]
    }