# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 21:49:51 2023

@author: nacho
"""

import streamlit as st
import json
import requests


# Define the endpoint of the FastAPI application
#endpoint = "https://PATOTradingCompany/backtest"

# Set the title of the Streamlit application
st.title("PATO🦆 : _Plataforma Analítica de Trading Online_")

# Create a text area for the user to input their brand name and a short description of their brand
st.header("Detalles de Inversión")
capital= st.number_input("Capital", min_value = 0)
mode = st.radio("Elige tu estrategia de Trading",["Scalping","Swing"])
risk = st.slider("Elige el riesgo aceptado",0,100)
win_loss_ratio = st.slider("Elige la proporción ganancia-pérdida",0,100)

if mode == "Swing":
    timeframe = st.radio("Elige el período de inversión",["1mo","2mo","3mo"])
else:
    timeframe = st.radio("Elige el período de inversión",["1d","2d","3d"])
        
ticker = st.radio("Elige una acción",["AAPL","TSLA","NVDA","AMZN","MSFT","PYPL","TSAT","PLTR","DIS","BABA","O","RGTI","MULN"])
st.subheader("Período de análisis")
start_date = st.date_input("Fecha Inicial")
end_date = st.date_input("Fecha Final")


# Prepare the input data for the API request
input = {"capital": float(capital),
         "risk":float(risk),
         "win_loss_ratio":float(win_loss_ratio),
         "timeframe":str(timeframe),
         "ticker":str(ticker),
         "mode":str(mode),
         "start_date":str(start_date),
         "end_date":str(end_date)
         }

# If the "Generate" button is clicked, send a request to the FastAPI application and display the response
if st.button("Calcular Ganancia"):
    res = requests.post(url="http://127.0.0.1:8000/backtest", data=json.dumps(input))
    #res_json = res.json()
    st.subheader(f"🚀🤑 Tu ganancia es 💲 {res}")
 
    
