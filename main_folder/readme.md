# This readme file give short description on how this repository should be used and how can we leverage each python file/result

## Mutiple_Report_To_Excel Folder
Contains python script which contains module of our extraction Algorithm, python file contains 3 main function: 1. extraction code 2. cleaning 3. sentiment analysis. This is the file we need to get the result stored in the extraction_result folder.

## Individual_file_extraction.py:

This file allows you to extract the MDA text from an individual filing. It takes the path to the filing as input and displays the extracted MDA text in the IDE.

## Bold_text.py:
an alternation of individual_File_extraction.py, in this code, MDA is extraction by using regular expression to search for heading occurances and stored in index, by locating headers index, we extract everything in between.

## Sentiment_analysis.py:

To use the code you need to input a clean MDA section to the function called 'evaluate'.
We first divided the clean MDA into sentences, then calculate the percentage of FLS to all sentences, and find a sentiment score of only FLS sentences.

## Regression.py
Contains our methodology on how we want to see the relation between stock price and word count
