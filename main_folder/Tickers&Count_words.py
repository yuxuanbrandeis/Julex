import requests
import pandas as pd

# create request header
headers = {'User-Agent': "hasanallahyarov@address.com"}

# get all companies data
companyTickers = requests.get(
    "https://www.sec.gov/files/company_tickers.json",
    headers=headers
    )

# dictionary to dataframe
companyData = pd.DataFrame.from_dict(companyTickers.json(),
                                     orient='index')



def count_words(input_string):
    # Remove leading and trailing whitespaces (optional)
    input_string = input_string.strip()

    # Split the string into words based on spaces (you can use other delimiters if needed)
    words_list = input_string.split()

    # Count the number of words in the list
    word_count = len(words_list)

    return word_count
                
