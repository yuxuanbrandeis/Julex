PartA&B.py:

This file contains the code to extract CIK numbers and perform MDA extraction for multiple filings within a folder structure. It saves the results in an Excel file. Make sure to specify the root directory containing the filings in the code.


Individual_file_extraction.py:

This file allows you to extract the MDA text from an individual filing. It takes the path to the filing as input and displays the extracted MDA text in the IDE.


Sentiment_analysis.py:

This is our first way to find a sentiment score, to use the code you need to input a clean MDA section to the function called 'evaluate'.
We first divided the clean MDA into sentences, then calculate the percentage of FLS to all sentences, and find a sentiment score of only FLS sentences.

