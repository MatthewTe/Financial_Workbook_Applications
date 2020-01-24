# Finance Data Analysis Python to Workbook Application
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
|---etf_data_transformation.py
|
|--excel_data_loading_package
|---__init__.py
|---dividend_etf_workbook.py
|
|--raw_data_extraction_package
|---web_based_financial_models.py
|
```
Each individual workbook project will be described as follows:
* Workbook Project name
  * Project Summary
  * Data Extraction
  * Data Transformation/Analysis
  * Data Loading to database and/or workbook
 
## List of Workbook ETL Packages in the Application: 
* #### [Dividend ETF Comparison Workshops](

## Dividend ETF Comparison Workbook 
* ### Dividend ETF Workbook Summary
The dividend ETF application is designed to perform data analysis and visualization on dividend Exchange Traded Products (ETPs). The application ingests data extracted from the web via the script web_based_financial_models.py. This data is then fed into the etf_data_transformation.py script where it is parsed and analyzed to show various metrics associated with dividend performance such as:
* Historical Annual Dividend Yields
* Maximum Dividend Drawdowns
* Dividend Volatility 
* ### Data Extraction
* ### Data Transformation/Analysis 
* ### Data Loading
 

