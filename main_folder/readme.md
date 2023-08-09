# This readme file give short description on how this repository should be used and how can we leverage each python file/result

## Mutiple_Report_To_Excel Folder
Contains python script which contains module of our extraction Algorith. That bunch of code, gives a final result of extraction, cleaning, sentiment analysis, adding prices, and regression based on multiple reports.

## Individual_file_extraction&cleaning.py:

This file containts 2 functions. 
1st helps to extract the MDA part from the indivdiual file. 
2nd helps to clean the extraction and make it possible to work on it with sentiments

## Bold_text.py:
an alternation of individual_File_extraction.py, in this code, MDA is extraction by using regular expression to search for heading occurances and stored in index, by locating headers index, we extract everything in between.

## Sentiment_analysis.py:

To use the code you need to input a clean MDA section to the function called 'evaluate'.
We first divided the clean MDA into sentences, then calculate the percentage of FLS to all sentences, and find a sentiment score of only FLS sentences.

## Regression.py
This file contains 2 bunches of codes.
1st helps to add stock prices of the filed_date and the day after based on yahoofinance API.
2nd helps to make a regression, where filed_date, tickers, and document type are represented as dummy variables. And the regression is based on how number of words affect the return of stock price.

## Document_Type&Count_Words.py

This file containts 2 functions:
1st is to find a document type of every report. Either it is 10-Q or 10-K
2nd is to count number of words of a given string, which we use for clean MDA.
