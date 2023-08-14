# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 21:33:28 2023

@author: nacho
"""

import pandas as pd
import numpy as np
import yfinance as yf
import talib




    
def backteststrategy(capital, risk_unit, win_loss_ratio, timeframe, ticker, mode, start_date, end_date):
    #Va a buscar datos a yahoo finance
        data = yf.download(ticker, start=start_date, end=end_date, interval=timeframe)
    #Genera columna con RSI
        data['RSI'] = talib.RSI(data['Close'], timeperiod=14)
    #Crea una columna con el indicador MACD
        data['MACD'], _, _ = talib.MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)

        total_trades = 0
        winning_trades = 0
        losing_trades = 0
        total_profit = 0
        initial_capital = capital
    
        for i in range(1, len(data)):
            if mode == "Scalping":
                if data['RSI'][i] > 70 and data['MACD'][i] > 0:
                    total_trades += 1
                    entry_price = data['Close'][i]
                    stop_loss = entry_price - risk_unit
                    take_profit = entry_price + (risk_unit * win_loss_ratio)
    
                    for j in range(i + 1, len(data)):
                        if data['High'][j] >= take_profit:
                            profit = take_profit - entry_price
                            total_profit += profit
                            winning_trades += 1
                            break
                        elif data['Low'][j] <= stop_loss:
                            loss = entry_price - stop_loss
                            total_profit -= loss
                            losing_trades += 1
                            break
            elif mode == "Swing":
                if data['RSI'][i] < 30 and data['MACD'][i] < 0:
                    total_trades += 1
                    entry_price = data['Close'][i]
                    stop_loss = entry_price - risk_unit
                    take_profit = entry_price + (risk_unit * win_loss_ratio)
    
                    for j in range(i + 1, len(data)):
                        if data['High'][j] >= take_profit:
                            profit = take_profit - entry_price
                            total_profit += profit
                            winning_trades += 1
                            break
                        elif data['Low'][j] <= stop_loss:
                            loss = entry_price - stop_loss
                            total_profit -= loss
                            losing_trades += 1
                            break
    
        final_capital = initial_capital + total_profit
        profitability = (total_profit / initial_capital) * 100
    
        months = max(len(data) // 30, 1)
        annualized_return = ((final_capital / initial_capital) ** (12 / months) - 1) * 100
    
        num_trades = total_trades
        num_winning_trades = winning_trades
        num_losing_trades = losing_trades
    
        results = {
            "Capital Inicial": initial_capital,
            "Capital Final": final_capital,
            "Rentabilidad (%)": profitability,
            "Rentabilidad Anualizada (%)": annualized_return,
            "Cantidad de operaciones": num_trades,
            "Cantidad de operaciones ganadoras": num_winning_trades,
            "Cantidad de operaciones perdedoras": num_losing_trades
        }
    
        return results
    
    
    
    
# Parámetros de ejemplo
capital = 10000
risk_unit = 2
win_loss_ratio = 2
timeframe = "1d"
ticker = "AAPL"
mode = "Swing"
start_date = "2019-01-01"
end_date = "2023-07-31"

# Ejecutar el backtest
backtest_results = backteststrategy(capital, risk_unit, win_loss_ratio, timeframe, ticker, mode, start_date, end_date)
print(backtest_results)
