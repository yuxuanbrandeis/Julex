import yfinance as yahooFinance
import pandas as pd

GetFacebookInformation = yahooFinance.Ticker("META")

pd.set_option('display.max_rows', None)

META_price = GetFacebookInformation.history(period="max")
print(META_price)
