# Importing webscraping packages:
import requests
import bs4
# Importing data management packages:
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import datetime
from datetime import timedelta
import time
import numpy as np
# Importing data vizualization packages:
import matplotlib.pyplot as plt
import seaborn as sns

sns.set() # Setting all charts to seaborn style
yf.pdr_override() # overiding pdr with yfinance packages


class Security(object):
    '''
    The Security object contains descriptive variables for each Security instance as well
    as the methods to retrive said variables from the web.
    Data is collected via the pandas_datareader package augmented with the yfinance
    package to allow data to be pulled directly from yahoo finance.
    If the Security is an Exchange Traded fund then holdings data is pulled from
    etfdb.com
    Parameters
    ----------
    ticker : str
        The string variable representing the ticker symbol for the Security. This
        string is the argument that is passed to all the data aggregation methods
    '''
    def __init__(self, ticker):

        # Declaring instance variables:
        self.ticker = ticker
        self.historical_prices = self.Price()
        self.price = round(self.historical_prices.iloc[-1]['Adj Close'], 2)

        # creating instance variable to store yfinance object:
        self.yFinance_object = yf.Ticker(self.ticker)

        # Storing specific instance variables forom yfinance object:
        self.dividend_history = self.yFinance_object.dividends
        self.title = self.yFinance_object.info['shortName']

        # Storing the historical returns dataframe:
        self.returns = self.returns()
        self.avg_return = self.returns.mean()
        self.std_return = self.returns.std()
        # Sharpe Ratio: 0.023 HISA savings account interest for risk free return
        self.sharpe_ratio = (self.avg_return - 0.023) / self.std_return

    def __repr__(self):
        return self.ticker

    def Price(self):
        '''Getting the historical price data of the ticker symbol
            from pandas_datareader
        Returns
        -------
        price : pandas dataframe
            The dataframe containing the historical price of the security from
            yahoo finance
        '''

        # Start/end date for pandas_datareader:
        start = datetime.datetime(1970, 1, 1) # Arbitrary start date
        end = datetime.datetime.today()

        # dataframe containing pricing data:
        price = pdr.get_data_yahoo(self.ticker, start, end)
        return price

    def returns(self):
        '''Method that takes the historical Adj Close price and converts it into
            a percent return on investment
        Returns
        -------
        Returns_df : pandas dataframe
            Dataframe containing the historical percent ROI for the ticker
        '''
        Returns_df = pd.DataFrame()

        # Creating column:
        Returns_df[self.ticker] = (self.historical_prices['Adj Close']).apply(
        lambda x : ((x - self.historical_prices['Adj Close'][0])) / self.historical_prices['Adj Close'][0])

        return Returns_df

class ETF(Security):
    '''
    ETF object represents an Exchange Traded Fund financial instrument. It is
    constructed as its parent class Security() and contains other fundemental
    data specific to the ETF financial instrument such as holdings data.
    Parameters
    ----------
    ticker : str
        The ticker string that is used to both initalize the parent class and to
        search for fundemental ETF data.
    '''

    def __init__(self, ticker):

        # Inheret parent __init__:
        super().__init__(ticker)

        # ETF holdings instance variables:
        self.holdings = self.build_holdings_df()

        # Constructing list of Security() objects from ETF ticker holdings:
        self.holdings_list = self.build_holdings_objects()

        # dataframe comparing the ROI of the ETF to its top 10 holdings:
        self.holdings_ROI = self.build_holdings_comparions()

    def build_holdings_df(self):
        '''Method uses pd.read_html to extract top 10 holdings table from
            Yahoo Finance website based on self.ticker
        Returns
        -------
        pd.read_html(url)[0] : pandas dataframe
            Dataframe containing the top 10 holdings of the ETF with: Name,
            Ticker symbol and % Allocation
        '''

        # Building the Yahoo Finance holdings tab url:
        url = "https://ca.finance.yahoo.com/quote/{self.ticker}/holdings?p={self.ticker}".format(self=self)

        # Creating a dataframe from the webpage:
        return pd.read_html(url)[0] # converting list of 1 df to dataframe

    def build_holdings_objects(self):
        '''Method that extracts a list of ticker symbols from the self.holdings
            dataframe and attempts to initalize each ticker as a Security() object
        Returns
        -------
        holdings_list : lst
            The list containing all the Security() objects from the self.holdings
            dataframe
        '''

        # Creating the main list:
        holdings_list = []

        # Calling the dataframe:
        df = self.holdings

        # iterating through the dataframe and appending to the list:
        for ticker in df['Symbol']:

            try: # attempting to initalize Security() object
                ticker = Security(ticker)

            except: # TODO: Write the ticker_cleaning method for exceptions:
                ticker = 'NaN'

            # Creating the list of Security() objects
            holdings_list.append(ticker)

        return holdings_list

    def build_holdings_comparions(self):
        '''Method extracts the performance of the top 10 holdings of an ETF and
            constructs a dataframe comparing the YTD performance of of each holding
            to the overall performance of the ETF
        Returns
        -------
        holdings_YTD_df : pandas dataframe
            The dataframe containing the YTD performance of each top 10 security
            holdings of the ETF and the YTD performance of the ETF
        '''

        # Creating dataframe:
        holdings_YTD_df = pd.DataFrame()

        holdings_YTD_df = self.returns

        # Adding columns to dataframe:
        holdings_YTD_df[self.ticker] = self.returns

        # Creating a df column for every holding in the Etf holdings list:
        for Security in self.holdings_list:

            try:
                holdings_YTD_df[Security.ticker] = Security.returns
            except:
                holdings_YTD_df['NaN'] = Security # TODO: Deal with erroring out

        # Really sketchy error handeling lol:
        holdings_YTD_df.drop(['NaN'], axis=1)

        # Converting 'NaN' values to 0 for visual clarity:
        holdings_YTD_df.fillna(0)

        return holdings_YTD_df
