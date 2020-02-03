# Finance Data Analysis Workbook Application
## Summary
The purpose of this application is to serve as a bundle of python scripts that- when executed perform ETL functions on the specified financial data. Special focus is placed on the “Loading” aspect of financial data pipelines, where, in addition to loading data to a database, the application uses transformed data to compile excel workbooks that summarize and present said financial data in a manner that is compliant with most standards for financial report formatting. 
#### In summary, this application is intended to serve as a bridge between the flexible data transformation python scripts/packages and the accessibility, simplicity and industry popularity of excel.
## Project Structure
The format/structure of the project is relatively basic and adheres to a common python project structure:

```
|-Application
|
|--__init__.py
|--excel_execution_script.py
|
|--data_transformation_package
|---__init__.py
|---dividend_data_transformation.py
|
|--statistical_data_validation_pkg
|---__init__.py
|---normality_testing.py
|
|--excel_data_loading_package
|---__init__.py
|---dividend_etf_workbook.py
|
|--raw_data_extraction_package
|---web_based_financial_models.py
|
```

## Data Validation Package and its use

Each individual workbook project will be described as follows:
* Workbook Project name
  * Project Summary
  * Data Extraction
  * Data Transformation/Analysis
  * Data Loading to database and/or workbook
 
## List of Workbook ETL Packages in the Application: 
* #### [Dividend ETF Comparison Workshops](https://github.com/MatthewTe/Financial_Workbook_Applications/blob/master/README.md#dividend-etf-comparison-workbook)

## Dividend ETF Comparison Workbook 
* ### Dividend ETF Workbook Summary
The dividend ETF application is designed to perform data analysis and visualization on dividend Exchange Traded Products (ETPs). The application ingests data extracted from the web via the script web_based_financial_models.py. This data is then fed into the etf_data_transformation.py script where it is parsed and analyzed to show various metrics associated with dividend performance such as:
* Historical Annual Dividend Yields
* Maximum Dividend Drawdowns
* Dividend Volatility 
* ### Data Extraction
The raw financial data that is fed into the rest of the data pipeline is obtained via the [finance web scraping package](https://github.com/MatthewTe/ETL-and-Statistical-Model-Validation-Packages/tree/master/finance_web_scraping_package) that power most financial analysis. 

* ### Data Transformation/Analysis 
Data transformation for divided data takes place via two main objects in the dividend_data_transformation.py script:

* dividend_asset()
* div_asset_comparison()

The web scraped data from the based finance models flows into these two objects and are transformed by various methods to produce the final data output that flows into the excel_data_loading package. Below is a diagram illustrating how dividend data flows through this transformation package:
![Image Not Found](https://github.com/MatthewTe/Financial_Workbook_Applications/blob/master/resources/Dividend%20Workbook%20Data%20Transformation%20chart.png)

Example of how to initialize the div_asset_comparison() object:
```pyhton
example = div_asset_comparison('WM, 'SPY', 'XOM')

print(example.ticker_dict)
print(example.annual_div_yields)
print(example.ticker_std)
print(example.ticker_pct_change)
print(example.max_annual_drawdown)
```

* ### Data Loading
 

