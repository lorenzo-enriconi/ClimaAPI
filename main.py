import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

API_KEY = "62ec1a83bac5c1c68bd48e9ef82b37c0"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_URL_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"

def chamar_api_clima(url: str, cidade: str, parametro_extra: dict | None = None) -> dict:
    parametros = {
        "q": cidade,
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt_br",
        **(parametro_extra or {})
    }
    
    try:
        resposta = requests.get(url, params=parametros, timeout=10, verify=False)
        if resposta.status_code != 200:
            return {
                "erro_externo": True,
                "conteudo_bruto": resposta.text[:200]
            }
        return resposta.json()
    except Exception as e:
        return {"erro_fatal": str(e)}
    
    
@app.get("/api/previsao")
def obter_previsao(cidade: str):
    return chamar_api_clima(BASE_URL, cidade)


@app.get("/api/clima")
def obter_clima(cidade: str):
    return chamar_api_clima(BASE_URL_FORECAST, cidade, {"cnt": 40})