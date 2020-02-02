# Importing data managment and transformation packages:
import pandas as pd
import numpy as np
import scipy
import scipy.stats as stats
import statsmodels.api as sm
# Importing data vizualization packages:
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib.pyplot as plt
# Misc packages imports:
import warnings


# Creating custom data validation warnings class:
class Data_Validation_Warning(UserWarning):
    pass

class normality_validation(object):
    """
    The normality_validation object is designed to perform visual and
    statistical tests to determine if the data conforms to a normal distribution.
    The tests are broken down into two main sections: visual and statistical.

    Methods
    -------
    visual_tests()
        This method performs both visual tests for normality on the dataframe:
        a histogram plot and a Quantile-Quantile Plnt

    shapiro_wilk_test()
        The method performs the shapiro-wilk test for normality.

    kolmogorov-smirnov_test()
        The method performs the Kolmogorov–Smirnov test for normality.

    # NOTE: When adding normality tests, UPDATE AT EVERY STAGE
    """

    def __init__(self, input_data, alpha, plot_indicator):
        """
        Parameters
        ----------
        input_data : Pandas dataframe/Series
            This is the dataframe that the normality tests will be performed on. The
            test is designed to perform analysis on a dataframe with a single column.

        alpha : float
            This is a float representing the level of significance for the statistical
            tests.

        """
        # Declaring instance variables:
        self.plot_indicator = plot_indicator
        self.data = input_data  # Converting df column to array
        self.alpha = alpha

        # Initalizing statistical normality tests:
        shapiro_wilk = self.shapiro_wilk_test()
        kol_smirnov = self.kolmogorov_smirnov_test()

        # Combining all of the dictionaries into a list for summary_df:
        summary_data = [shapiro_wilk, kol_smirnov]

        summary_df = pd.DataFrame(summary_data,
        index= ['Shapiro-Wilk Test', 'Kolmogorov-Smirnov test'])

        # Declaring as instance:
        self.summary_df = summary_df

        # Raises Warnings if data failes Gaussian Validation tests:
        if shapiro_wilk['Gaussian indicator'] != True:
            warnings.warn('Data does not pass Shapiro-Wilk Test of Gaussian \
distribution- Data may not be normally distributed',
             Data_Validation_Warning)
        else:
            pass

        if kol_smirnov['Gaussian indicator'] != True:
            warnings.warn('Data does not pass Kolmogorov-Smirnov Test of Gaussian \
distribution- Data may not be normally distributed',
             Data_Validation_Warning)

        # Initalize the visual normality test if the indicator = True:
        if plot_indicator == True:
            self.visual_tests()

        else:
            pass

    def visual_tests(self):
        '''Plots the visual normality tests for the dataframe. Prints all
        graphs as multiple axis on a single matplotlib figure. Graphical
        normality tests are:

        Histogram Plot

        Quantile-Quantile Plot
        '''

        # Declaring the number of axis for subplots:
        fig = plt.figure('Normality Test Summary for ' + self.data.name + ' Data ')
        # adding gridspec:
        gs = fig.add_gridspec(2, 2)

        # Plotting histogram as ax1:
        ax1 = fig.add_subplot(gs[0,0])
        #ax1.set_title('Histogram')
        self.data.hist(grid=True, ax=ax1)
        plt.title(self.data.name + ' Column Data Histogram ')

        # Creating a Q-Q plot as ax2:
        ax2 = fig.add_subplot(gs[0,1])
        ax2.set_title(self.data.name + ' Column Data Q-Q Plot')
        sm.qqplot(self.data, scale=3,line='s', ax=ax2) # TODO:: Look into QQ, question accuracy

        # Adding summary_df table from __init__ method:
        ax3 = fig.add_subplot(gs[0, :])
        ax3.axis('off')
        # matplotlib table format:
        table = plt.table(cellText=self.summary_df.values, rowLabels=self.summary_df.index,
        colLabels=self.summary_df.columns, cellLoc='center')
        # Formatting:
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1,2)



        fig.tight_layout()
        plt.show()

    def shapiro_wilk_test(self):
        '''This method performs the shapiro_wilk_test for normality of the
        dataset. It reutrns a dictionary that contains the following information:

        - The shapiro-wilk test statistic
        - The p value
        - The alpha value (typically 0.05)
        - A boolean value indicating if the sample appears Gaussian
            (True == Gaussian- Fail to reject H0, False =! Gaussian- Reject H0)

        Returns
        -------
        shapiro_dict : dictionary
            A dictionary containing the following results data from the shapiro
            test.
        '''

        # Perfomring shapiro-wilk test using scipy:
        # Assigning the test-stat variable and the p-value:
        shapiro_test_stat, p_value = stats.shapiro(self.data)

        # Conditional that declares the Gaussian_bool if the p-value fails to reject
        # alpha level:
        if p_value > self.alpha:

            Gaussian_bool = True

        else:

            Gaussian_bool = False

        # Constructing a dictionary of result data to return:
        shapiro_dict = {'test statistic' : shapiro_test_stat,
                        'p value': p_value, 'alpha': self.alpha,
                        'Gaussian indicator': Gaussian_bool }


        return shapiro_dict

    def kolmogorov_smirnov_test(self):
        '''This method performs the kolmogorov-smirnov_test for normality of the
        dataset. It reutrns a dictionary that contains the following information:

        - The kolmogorov-smirnov_test test statistic
        - The p value
        - The alpha value (typically 0.05)
        - A boolean value indicating if the sample appears Gaussian
            (True == Gaussian- Fail to reject H0, False =! Gaussian- Reject H0)

        Returns
        -------
        smirnov_test_dict : dictionary
            A dictionary containing the following results data from the
            kolmogorov-smirnov_test.
        '''

        # Performing the kolmogorov_smirnov_test and declaring variables:
        smirnov_test_stat, p_value = stats.kstest(self.data, 'norm', args=(
        np.mean(self.data), np.std(self.data))) # Standardized to the data's mean and std.

        # Conditional Statement determining if the Gaussian_indicator is True or false:
        if p_value > self.alpha:

            Gaussian_bool = True

        else:

            Gaussian_bool = False

        # Constructing the smirnov_test_dict:
        smirnov_test_dict = {'test statistic' : smirnov_test_stat,
                            'p value': p_value, 'alpha': self.alpha,
                            'Gaussian indicator': Gaussian_bool }

        return smirnov_test_dict
