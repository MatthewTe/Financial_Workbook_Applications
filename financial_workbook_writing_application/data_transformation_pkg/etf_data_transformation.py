# Path hack:
import sys
sys.path.append('..')

# Importing web scraping objects from raw_data_extraction_pkg:
from financial_workbook_writing_application.raw_data_extraction_pkg\
.web_based_financial_models import Security

# Importing data management packages:
import pandas as pd
from collections import Counter


# TODO: CHANGE BOTH THE PACKAGE AND THE OBJECTS TO DIVIDEND STOCKS NOT JUST DIVIDEND ETFS.

# Creating the class that stores the ETF data transformation:
class dividend_etf(Security):
    """
    This object performs data analysis from data inhereted from
    raw_data_extraction_pkg's Security object. It transforms data into the
    dataframes necessary to evaluate an ETF's dividend performance and compare
     said peformance to other ETPs.

    Methods
    ---------
    build_hist_div_yields()
        Returns a dataframe containing the historical quarterly dividend yield.

    build_annual_div_yields()
        Returns a dataframe containing the historical annual dividend yield.
    """

    def __init__(self, ticker):
        """
        Parameters
        ----------
        ticker: str
            This is the ticker string that is used to initalize the parent
            Security() object. It provides all the data necessary to perform
            futher analysis.

            NOTE: This ticker MUST be of an Exchange Traded Fund (ETF). This
            object was not designed for any other asset class.

        """

        # Inherent parnet __init__ for web_based_financial_models Security():
        super().__init__(ticker)

        # Quarterly and annual dividend yield:
        self.hist_div_yields = self.build_hist_div_yields()
        self.annual_div_yields = self.build_annual_div_yields()

        # TODO: Add Dividend Histogram and other Div vol plots.


    def build_hist_div_yields(self):
        '''Returns a dataframe containing the historical dividend yields of the ETF
        based on the historical_prices dataframe inhereted by the parent Security
        object.

        Returns
        -------
        hist_div_df : pandas dataframe
            The dataframe containing all the dividend yields against historical
            timeseries.
        '''
        # Merging historical pricing data with absoloute dividend payments:
        Adj_close = pd.DataFrame(self.historical_prices['Close'])
        div_payments = Adj_close.merge(self.dividend_history, left_index=True,
        right_index=True)

        # Creating new div_payments column to show % Yield:
        div_payments['% Yield'] = (div_payments['Dividends'] /
        div_payments['Close'])*100

        # Renaming:
        hist_div_df = div_payments

        return hist_div_df


    def build_annual_div_yields(self):
        '''Returns a dataframe containing the annual dividend yields of the ETF
        based on the historical_prices dataframe inhereted by the parent Security
        object.

        Returns
        -------
        annual_div_df : pandas dataframe
             The dataframe containing the annual dividend yields against historical
             timeseries.
        '''

        # Creating dataframe with only time series divided yield:
        percent_yield = self.hist_div_yields

        # Grouping the % Yield by year:
        grouped_yield_df = percent_yield.groupby(pd.Grouper(freq='Y')).sum()
        grouped_yield_df.index = grouped_yield_df.index.year

        # Creating a list of all the years in which dividends were paid:
        year_list = grouped_yield_df.index
        ungrouped_year_list = percent_yield.index.year

        # Parsing grouped_yield_df to remove any years that do not have 4 quarters
        # do to them potentally skewing the data in future calculations:
        counted_years_list = Counter(ungrouped_year_list)

        # For loop that tests each year for 4 quarters and removes the rest:
        for x in year_list:

            if counted_years_list[x] != 4:
                grouped_yield_df.drop(x, inplace=True)

            else:
                pass

        # Removing all unnecessary columns for final df return:
        annual_div_df = grouped_yield_df['% Yield']

        return annual_div_df










# Test = print(dividend_etf('XOM').annual_div_yields)
