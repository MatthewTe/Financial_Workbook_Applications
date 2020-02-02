# Path hack:
import sys
sys.path.append('..')

# Importing web scraping objects from raw_data_extraction_pkg:
from financial_workbook_writing_application.raw_data_extraction_pkg\
.web_based_financial_models import Security

# Importing data validation objects from statistical_data_validation_pkg:
from financial_workbook_writing_application.statistical_data_validation_pkg\
.normality_testing import normality_validation as normality

# Importing data management packages:
import pandas as pd
from collections import Counter
import numpy as np

# Importing data vizualization packages:
import matplotlib as mpl
import matplotlib.pyplot as plt



# Creating the class that stores the asset data transformation:
class dividend_asset(Security):
    """
    This object performs data analysis from data inhereted from
    raw_data_extraction_pkg's asset object. It transforms data into the
    dataframes necessary to evaluate an asset's dividend performance and compare
     said peformance to other ETPs.

    Methods
    ---------
    build_hist_div_yields()
        Returns a dataframe containing the historical quarterly dividend yield.

    build_annual_div_yields()
        Returns a dataframe containing the historical annual dividend yield.

    build_max_drawdown()
        Returns a float that represents the largest reduction in divided yield.

    build_dividend_volatility()
        The method contains a dictionary containing all the dividend volatility
         metrics.
    """

    def __init__(self, ticker, plot):
        """
        Parameters
        ----------
        ticker: str
            This is the ticker string that is used to initalize the parent
            asset() object. It provides all the data necessary to perform
            futher analysis.

            NOTE: This ticker MUST be of an Exchange Traded Fund (asset). This
            object was not designed for any other asset class.

        plot : bool
            This boolean indicator is used to dictate if any of the validation
            tests plot their outputs or not.
        """

        # Inherent parnet __init__ for web_based_financial_models asset():
        super().__init__(ticker)
        self.plot = plot

        # Quarterly and annual dividend yield:
        self.hist_div_yields = self.build_hist_div_yields()
        self.annual_div_yields = self.build_annual_div_yields()

        # Dividend Data Analysis:
        self.max_drawdown = self.build_max_drawdown()
        self.dividend_volatility = self.build_dividend_volatility()


    def build_hist_div_yields(self):
        '''Returns a dataframe containing the historical dividend yields of the asset
        based on the historical_prices dataframe inhereted by the parent asset
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
        '''Returns a dataframe containing the annual dividend yields of the asset
        based on the historical_prices dataframe inhereted by the parent asset
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

        # Renaming % Yield for comparison purposes in data viz/load package:
        annual_div_df.rename(self.ticker, inplace=True)

        return annual_div_df

    def build_max_drawdown(self):
        '''Returns a dictionary that contains both the maximum decrease of
        dividend % yield in a single year and qualterly

        The data is provided by the build_annual_div_yields() and hist_div_yields()
        methods and the data is parsed using the numpy data packag and is
        represented as a positive float.

        Returns
        --------
        drawdown_dict : dictionary
            The dictionary containing the maximum divided drawdowns annualy and
            quarterly:

            {max_quarterly_drawdown, max_annual_drawdown}
        '''

        # Anual Drawdown:

        # Calculating the diff between consecutive elements:
        difference = np.diff(self.annual_div_yields)
        # Formatting difference list:
        difference_list = [round(x, 3) for x in difference] # rounding
        # Selecting the lowest value of the list:
        max_annual_drawdown = min(difference_list) * -1 # represented as a positive float


        # Quarterly Drawdown:

        # Calculating the diff between consecutive elements:
        difference = np.diff(self.hist_div_yields['% Yield'])
        # Formatting difference list:
        difference_list = [round(x, 3) for x in difference] # rounding
        # Selecting the lowest value of the list:
        max_quarterly_drawdown = min(difference_list) * -1 # represented as a positive float


        # Creating and returning drawdown_dict:
        drawdown_dict = {'max_quarterly_drawdown': max_quarterly_drawdown,
                        'max_annual_drawdown': max_annual_drawdown}

        return drawdown_dict

    def build_dividend_volatility(self):
        '''Method calculates and returns a dictionary describing the volatility
        of the divided yield for the security such as:
        - Standard Deviation
        - % Yield
        - Percent Change of % Yield

        Note - All volatility is of annual data.

        Returns
        -------
        volatility_dict : A dictionary containing all the dividend volatility
        metrics:
        {pct_yield: pct_yield, divided_std: divided_std, div_pct_change: div_pct_change}
        '''

        # Performing data validation before transformation:
        pct_yield = self.annual_div_yields # Extracting series from df.
        alpha = 0.05
        normality(self.annual_div_yields, alpha, self.plot)

        # Generating standard deviation:
        divided_std = pct_yield.std()

        # Calculating the 'pct_change' of the % Yield column:
        div_pct_change = pct_yield.pct_change()


        # Creating and returning the dictionary that the method returns:
        volatility_dict = {'pct_yield': pct_yield, 'divided_std': divided_std,
        'div_pct_change': div_pct_change}

        return volatility_dict

# Test = dividend_asset('SPYD', True)

class div_asset_comparison(object):
    """
    The object stores the methods that construct the agreate dataframes
    used for the comparison of divided yield generating assets.

    Methods
    -------
    annual_div_yield_aggregator()
        The method returns a dataframe containing the annual divided yields of
        all the ticker symbols input.

    std_aggregator()
        The method aggregates all the standard deviation values for each asset's
        divided yield compiles them into a dictionary.

    pct_change_aggregator()
        The method returns a dataframe that aggregates all the percent changes
        in divided yields for each ticker.

    max_annual_drawdown_aggregator()
        The method returns a dictionary containing the max annual divided yield
        drawdown, indexed by ticker name

    """

    def __init__(self, *tickers):
        """
        Parameters
        ----------
        *tickers : str
            A string representing the ticker symbol of the divided asset that
            will be initalized by the dividend_asset() object. Each dataframe
            generated by this object will be a comparitive dataframe that
            compares each tiker input in the *ticker argument.
        """

        # Initalizing a dictionary that contains all the ticker objects:
        self.ticker_dict = {}

        # Initalizing every ticker input as a dividend_asset() object and storing
        # them in an instance dictionary:
        for ticker in tickers:
            # Initalizing object:
            div_obj = dividend_asset(ticker, False)

            self.ticker_dict.update({div_obj.ticker: div_obj})


        # Initalizing instance variables:
        self.annual_div_yields = self.annual_div_yield_aggregator()
        self.ticker_std = self.std_aggregator()
        self.ticker_pct_change = self.pct_change_aggregator()
        self.max_annual_drawdown = self.max_annual_drawdown_aggregator()


    def annual_div_yield_aggregator(self):
        '''Aggregates the annual divided yields of each ticker input and
        compiles them into a dataframe indexed by year

        Returns
        -------
        aggregated_yield : pandas dataframe
            The dataframe containing the annual divided yields of each
            ticker input into the argument indexed by year.
        '''

        # Creating main dataframe
        agg_div_df = pd.DataFrame()

        for ticker in self.ticker_dict:
            agg_div_df = agg_div_df.append(self.ticker_dict[ticker].annual_div_yields)

        # Transposing dataframe and dropping all NaN data:
        aggregated_yield = agg_div_df.T # NOTE: think about .dropna()

        # Resorting by year:
        aggregated_yield.sort_index(inplace=True)

        return aggregated_yield

    def std_aggregator(self):
        '''The method aggregates the standard deviations of the divided yields of
        every asset indicated by the tickers in self.ticker_dict

        Returns
        -------
        aggregate_std : dict
            The pandas dataframe that contains all the standard deviation values
            for each ticker in the ticker_df
        '''

        # Creating aggregate_std dataframe:
        aggregate_std_dict = {}

        # Itterative loop that appends each value to the dataframe:
        for ticker in self.ticker_dict:
            aggregate_std_dict.update({ticker : self.ticker_dict[ticker].dividend_volatility['divided_std']})

    def pct_change_aggregator(self):
        '''The method aggregates the percent change of the % Dividend Yield for
        each ticker symbol and returns it as a dataframe.

        Returns
        -------
        agg_pct_change_df : pandas dataframe
            The pandas dataframe that contains the percent change of the % Dividend
            Yield for each ticker symbol indexed by year.
        '''

        agg_pct_change_df = pd.DataFrame()

        # Itterative loop that adds pct_chage dataframes together:
        for ticker in self.ticker_dict:
            agg_pct_change_df = agg_pct_change_df.append(self.ticker_dict[ticker].dividend_volatility['div_pct_change'])

        # Transposing dataframe:
        agg_pct_change_df = agg_pct_change_df.T

        # Resorting by date:
        agg_pct_change_df.sort_index(inplace=True)

        return agg_pct_change_df

    def max_annual_drawdown_aggregator(self):
        '''The method aggregates the maximum annual divided drawdown of each
        divided asset in a dictionary, indexed by ticker symbol.

        Returns
        -------
        agg_div_drawdown_dict : dictionary
            A dictionary containing the max annual yield drawdown of each asset
            indexed by ticker symbol
        '''

        # Creating empty dict:
        agg_div_drawdown_dict = {}

        # Itterator that appends each drawdown data point to the dict:
        for ticker in self.ticker_dict:
            agg_div_drawdown_dict.update({ticker :
             self.ticker_dict[ticker].max_drawdown['max_annual_drawdown']})

    
        return agg_div_drawdown_dict


div_asset_comparison('WM', 'SPY', 'XOM')
