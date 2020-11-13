import yfinance as yf
import streamlit as st
import pandas as pd
import datetime
import pandas as pd
import numpy as np
import mplfinance as mpf
from cad_tickers.sedar.tsx import  get_ticker_filings

st.write("""
# Stock Docs vs Price

Plotting filings reports against price.
""")

st.sidebar.header('User Input Parameters')

today = datetime.date.today()
def user_input_features():
    ticker = st.sidebar.text_input("Ticker", 'PKK.CN')
    webticker = st.sidebar.text_input("Web Ticker", 'PKK:CNX')
    start_date = st.sidebar.text_input("Start Date", '2014-01-01')
    end_date = st.sidebar.text_input("End Date", f'{today}')
    return ticker, webticker, start_date, end_date

ticker, webticker, start_date, end_date = user_input_features()

def get_yfinance_data(ticker, start_date, end_date):
    data = yf.download(ticker, start_date, end_date)
    return data

# Add more error handling
# when nothing is returned
def get_filings(ticker):
    filings_resp = get_ticker_filings("PKK:CNX", fromDate="2015-11-11", toDate="2020-11-11", limit=1000)
    filings = filings_resp.get('filings')
    return filings

def get_matched_filings(filings):
    # Iteration
    report_matches = ["financial", "Audited"]
    matched_filings = []
    for file in filings:
        # scan for words in substring
        file_name = file['name']
        if any(x in file_name for x in report_matches):
            matched_filings.append(file)
    return matched_filings

data = get_yfinance_data(ticker, start_date, end_date)
filings = get_filings(webticker)
matched_filings = get_matched_filings(filings)


filings_date = [ file['filingDate'] for file in matched_filings]
filings_date.sort()
cmc = yf.Ticker(ticker)
data = cmc.history(interval="1d", start=start_date, end=end_date)

close = data["Close"]
data['Rolling'] = data['Close'].rolling(30).mean()
# Make blank new dataframe to add markers to
filings_df = pd.DataFrame(index=data.index)
filings_df["Close"] = np.nan

filings_fmt_dates = [pd.Timestamp(file_date) for file_date in filings_date]
# filings_data_points = [close.at[date] for date in filings_fmt_dates]
for filing_date in filings_fmt_dates:
  # filings_df.loc[filing_date]['Close'] = close.at[filing_date]
  filings_df.loc[filing_date]['Close'] = data.loc[filing_date, 'Rolling']


earnings_date = mpf.make_addplot(filings_df, type='scatter', markersize=200,marker='^',panel=1)
fig, ax = mpf.plot(
    data,
    addplot=earnings_date,
    returnfig=True
)

st.pyplot(fig)
