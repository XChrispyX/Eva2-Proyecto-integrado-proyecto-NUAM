from fastapi import FastAPI
import requests

app = FastAPI(
    title="Servicio de Monedas NUAM",
    description="Microservicio para obtener valores de COL, CLP, SOL y UF.",
    version="1.0.0",
)

# Valores por defecto en caso de error con la API externa
DEFAULT_VALUES = {
    "CLP": 1,
    "COL": 0.004,     # ejemplo
    "SOL": 0.0035,    # ejemplo
    "UF": 0.000027,   # ejemplo
}


@app.get("/api/monedas/")
def obtener_monedas():
    """
    Consulta una API externa HTTPS (open.er-api.com) para obtener tasas de cambio
    con base CLP. Si falla, usa valores por defecto.
    """
    url = "https://open.er-api.com/v6/latest/CLP"

    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()

        # La API trae las tasas en data["rates"]
        rates = data.get("rates") or {}

        col = rates.get("COP")
        sol = rates.get("PEN")
        uf = rates.get("CLF")

        # Si faltan datos, usamos fallback para que nunca haya null
        if col is None or sol is None or uf is None:
            print("⚠ API no entregó todas las monedas, usando valores por defecto")
            return {
                "CLP": DEFAULT_VALUES["CLP"],
                "COL": col or DEFAULT_VALUES["COL"],
                "SOL": sol or DEFAULT_VALUES["SOL"],
                "UF": uf or DEFAULT_VALUES["UF"],
                "source": "default_partial",
            }

        # Caso ideal: datos reales de la API
        print("✅ Datos de API usados correctamente")
        return {
            "CLP": 1,
            "COL": col,
            "SOL": sol,
            "UF": uf,
            "source": "api",
        }

    except Exception as e:
        print("❌ Error consultando API de monedas:", e)
        # Fallback total
        return {
            **DEFAULT_VALUES,
            "source": "default_error",
        }