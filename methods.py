import math
from data import *
# https://www.omnicalculator.com/finance/intrinsic-value
# https://www.fool.com/investing/how-to-invest/stocks/discounted-cash-flow-model/
# http://www.moneychimp.com/articles/valuation/dcf.htm


def dcf(stock: str):
    eps = getEPS(stock)

    y1 = 5  # grow at growth rate for y1 years
    g1 = 7.79/100  # growth rate
    g2 = 5/100  # level off to annual growth rate
    Kc = getMarketAnnualReturn()/100  # market benchmark

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


a = dcf('AAPL')
print(a)
