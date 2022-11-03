import requests
import yfinance as yf


def getWacc(stock: str):
    response = requests.get(
        'https://www.gurufocus.com/term/wacc/'+stock+'/WACC-Percentage/')
    index1 = response.text.find('weighted average cost of capital is')+44
    index2 = response.text.find('%', index1)
    return float(response.text[index1:index2])


def getEPS(stock: str):
    ticker = yf.Ticker(stock)
    return ticker.info['trailingEps']


def getMarketPrice(stock: str):
    ticker = yf.Ticker(stock)
    return ticker.info['regularMarketPrice']


def getMarketAnnualReturn():
    returns = [-20.09, 28.71, 18.4, 31.49, -4.38, 21.83, 11.96,
               1.38, 13.69, 32.39, 16, 2.11, 15.06, 26.46, -37, 5.49]
    return (sum(returns)/len(returns))
