# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 21:39:43 2023

@author: nacho
"""

import io
import uvicorn
import numpy as np
import nest_asyncio
from enum import Enum
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel


from PATOBack import backteststrategy


app = FastAPI(title='PATO Trading')


class StrategyParameters(BaseModel):
    capital: float
    risk_unit: float
    win_loss_ratio: float
    timeframe: str
    ticker: str
    mode: str
    start_date: str
    end_date: str
    
    

@app.get("/")
async def hola():
    return "Bienvenido a PATO: Plataforma Analìtica de Trading Online"


@app.get("/about")
async def descripcion():
    return "La economía esta cada vez más complicada para las personas, con inflaciones históricas y eventos globales que impactan con volatilidades gigantes que han causado que la gente busque formas para sobrevivir al hostil contexto ecnomómico. Hoy en día los instrumentos tradicionales como los fondos mutuos y depósitos a plazo fijo no están logrando rendimientos mejores que la inflación, lo que está perjudicando a los inversionistas minoristas, quienes necesitan nuevas alternativas de inversión. Nuestro proyecto busca resolver este problema proporcionando una plataforma de datos en tiempo real que visualiza el rendimiento de varios indicadores técnicos y estrategias de trading para que los inversionistas puedan invertir de forma oportuna y respaldados por análisis."


@app.post("/backtest")
async def run_backtest(parameters: StrategyParameters):
    try:
        
        results = backteststrategy(parameters.capital, parameters.risk_unit, parameters.win_loss_ratio,
                                parameters.timeframe, parameters.ticker, parameters.mode,
                                parameters.start_date, parameters.end_date)
        
        print(results['Capital Final'])
        
    except Exception as e:
        print(e)
        return e
    
    return results['Capital Final']






nest_asyncio.apply()

# Donde se hospedará el servidor
host = "127.0.0.1"

# ¡Iniciemos el servidor!
uvicorn.run(app, host=host, port=8000)