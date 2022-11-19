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


def getFreeCashFlow(stock: str):
    ticker = yf.Ticker(stock)
    cashflow = ticker.cashflow
    fcf = cashflow.loc['Total Cash From Operating Activities'] + \
        cashflow.loc['Capital Expenditures']
    return [float("{:.2f}".format(x)) for x in fcf.to_numpy()]


def getBeta(stock: str):
    ticker = yf.Ticker(stock)
    return ticker.info['beta']


def getRiskFreeRate():
    response = requests.get(
        url='https://ycharts.com/indicators/1_year_treasury_rate', headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh;'})

    index1 = response.text.find('<p>1 Year Treasury Rate is at ')+30
    index2 = response.text.find('%', index1)
    return float(response.text[index1:index2])


def getMarketMonthlyReturn():
    response = requests.get(
        url='https://ycharts.com/indicators/sp_500_monthly_return', headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh;'})

    index1 = response.text.find('<p>S&amp;P 500 Monthly Return is at ')+36
    index2 = response.text.find('%', index1)
    return float(response.text[index1:index2])
