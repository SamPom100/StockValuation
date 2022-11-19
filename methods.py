import math
from data import *
import sys
# https://www.omnicalculator.com/finance/intrinsic-value
# https://www.fool.com/investing/how-to-invest/stocks/discounted-cash-flow-model/
# http://www.moneychimp.com/articles/valuation/dcf.htm


def dcf(stock: str):
    eps = getEPS(stock)

    y1 = 5  # grow at growth rate for y1 years
    g1 = 7.79/100  # growth rate
    g2 = 5/100  # level off to annual growth rate

    returns = [-20.09, 28.71, 18.4, 31.49, -4.38, 21.83, 11.96,
               1.38, 13.69, 32.39, 16, 2.11, 15.06, 26.46, -37, 5.49]
    tmp = (sum(returns)/len(returns))
    Kc = tmp()/100  # market benchmark

    v1 = eps*geomSeries((1 + g1)/(1 + Kc), 1, y1)
    v2 = futureValue(eps, g1, y1)*(1 + g2)/(Kc - g2)
    v = v1 + presentValue(v2, Kc, y1)
    return v


def geomSeries(z, m, n):
    amt = 0
    if (z == 1.0):
        amt = n + 1
    else:
        amt = (math.pow(z, n + 1) - 1)/(z - 1)
    if (m >= 1):
        amt -= geomSeries(z, 0, m-1)
    return amt


def futureValue(p, r, y):
    return p * math.pow(1+r, y)


def presentValue(fv, r, y):
    return fv/math.pow(1+r, y)


def cashFlowValuation(stock: str):
    ticket = yf.Ticker(stock)
    outstandingshares = ticket.info['sharesOutstanding']

    beta = getBeta(stock)
    adjusted_beta = (1-0.3333) * beta + 0.3333
    risk_free_rate = getRiskFreeRate()/100  # 1 year treasury bill rate
    market_return = getMarketMonthlyReturn()/100  # 1 year S&P 500 return / 12
    expected_return = (risk_free_rate +
                       adjusted_beta * (market_return - risk_free_rate))

    required_rate = expected_return
    perpetual_rate = 0.02
    cashflow_growthrate = 0.03

    years = [1, 2, 3, 4]

    freecashflow = getFreeCashFlow(stock)
    freecashflow.reverse()

    futurefreecashflow = []
    discountfactor = []
    discountedfuturecashflow = []

    terminalvalue = freecashflow[-1] * \
        (1 + perpetual_rate) / (required_rate - perpetual_rate)

    for year in years:
        cashflow = freecashflow[-1] * (1 + cashflow_growthrate) ** year
        futurefreecashflow.append(cashflow)
        discountfactor.append((1 + required_rate) ** year)

    for i in range(0, len(years)):
        discountedfuturecashflow.append(
            futurefreecashflow[i] / discountfactor[i])

    discountedterminalvalue = terminalvalue/(1+required_rate)**len(years)
    discountedfuturecashflow.append(discountedterminalvalue)

    todayvalue = sum(discountedfuturecashflow)
    fairvalue = todayvalue/outstandingshares

    marketPrice = getMarketPrice(stock)
    print(f'The Market Price of {stock} is ${marketPrice}')
    print(f'The Fair Value is ${fairvalue:.2f}')
    if (marketPrice > fairvalue):
        print(f"It's Overvalued by ${marketPrice - fairvalue:.2f}")
    else:
        print(f"It's Undervalued by ${fairvalue - marketPrice:.2f}")
