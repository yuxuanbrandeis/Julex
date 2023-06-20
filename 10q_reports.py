
## pip install sec-api 
## pip install bs4
## This is example is for AAPLE between 2001-2023
from sec_api import QueryApi

# your API key
api_key = "41f238fdae7e3b5ae0cbcdae8f8d04fa61fd2d91e6ab9ab28f40c2d63173c6f4"

# create QueryApi object
queryApi = QueryApi(api_key=api_key)

# initial query parameters
start_from = 0
size = 1000  # adjust this based on the API's maximum limit

all_filings = []

while True:
    # define the query
    query = {
        "query": { 
            "query_string": {
                "query": "ticker:AAPL AND filedAt:{2001-01-01 TO 2023-12-31} AND formType:\"10-Q\""
            } 
        },
        "from": str(start_from),
        "size": str(size),
        "sort": [{ "filedAt": { "order": "desc" } }]
    }

    # fetch the filings
    filings = queryApi.get_filings(query)

    # break if no more filings
    if not filings['filings']:
        break

    # add filings to the all_filings list
    all_filings.extend(filings['filings'])

    # increment the start_from
    start_from += size


## all Filings for every period is saved in all_filings, we can see there are 70 but total reports for those periods are 69 on Edgar
## The reason is  at 2006 3rd quarter Aaple didnt do the report and instead they have a document explanin the reason
# print the total number of filings
print(f"Total filings returned: {len(all_filings)}")


## Show all filings for the first item (Companyname,Link, Date,CIK,FormType and etc.) This one will show for the last quarter report which is 2023-05-04
all_filings[0]

## Extract the link to .txt for the 2023-05-04 Quarter report
link=all_filings[0]['linkToTxt']


# %%% 

## We will extract only the .txt for 2023-05-04 which we took from the 1st part as an example.
## this part helps to extract MDA part from the whole .txt file, however it is still extracting as part of html with html syntaxes
from sec_api import ExtractorApi

extractorApi = ExtractorApi(api_key)

filing_url_10q = link

extracted_section_10q = extractorApi.get_section(filing_url_10q, "part1item2", "text")

extracted_section_10q


## Here, we take the extracted part which had html indexes and do html parsing, so that we can have the clean text.
from bs4 import BeautifulSoup

html_text = extracted_section_10q
# Create a BeautifulSoup object
soup = BeautifulSoup(html_text, 'html.parser')

# Extract the text content without HTML tags
text = soup.get_text()

print(text)


## Later adding "for" loop, we can go through all of the links which are given by the 1st part of the code 
## and save them to a dictionary and then download it.

