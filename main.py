import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

proxy = "http://lorenzo-enriconi:Sexta04042003$@proxyprx.ipesaude.intra.rs.gov.br:3128"

os.environ['HTTP_PROXY'] = proxy
os.environ['HTTPS_PROXY'] = proxy

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

@app.get("/api/previsao")
def obter_previsao(cidade: str):
    parametros = {
        "q": cidade,
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt_br",
        "cnt": 40
    }
    
    try:
        resposta = requests.get(BASE_URL_FORECAST, params=parametros, timeout=10, verify=False)
        return resposta.json()
    except Exception as e:
        return {"erro_fatal": str(e)}


@app.get("/api/clima")
def obter_clima(cidade: str):

    parametros = {
        "q": cidade,
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt_br"
    }
  
    try:
        resposta = requests.get(BASE_URL, params=parametros, timeout=10, verify=False)
        # Se a API externa retornar erro (401, 404, etc), isso vai nos mostrar
        if resposta.status_code != 200:
            return {
                "erro_externo": True,
                "conteudo_bruto": resposta.text[:200]
            }
            
        return resposta.json()
    
    except Exception as e:
        return{"erro_fatal": str(e)}