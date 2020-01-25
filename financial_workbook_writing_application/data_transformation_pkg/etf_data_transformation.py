# Path hack:
import sys
sys.path.append('..')

# Importing web scraping objects from raw_data_extraction_pkg:
from financial_workbook_writing_application.raw_data_extraction_pkg\
.web_based_financial_models import Security

# Importing data management packages:
import pandas as pd


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

        """

        # Inherent parnet __init__ for web_based_financial_models Security():
        super().__init__(ticker)

        # Quarterly and annual dividend yield:
        self.hist_div_yields = self.build_hist_div_yields()
        self.annual_div_yields = self.build_annual_div_yields()


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
        # TODO: WRITE METHOD

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
        # TODO: WRITE METHOD

Test = dividend_etf('TAN')
#print(Test.historical_prices)
