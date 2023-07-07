# COMPANY CONFORMED NAME: Matson, Inc.
# CENTRAL INDEX KEY: 0000003453
# Sub-string method

import nltk

def extract_mda_section(file_path, title1, title2):
    with open(file_path, 'r') as file:
        content = file.read()

    positions = []
    index = 0

    while index < len(content):
        start_index = content.find(title1, index)
        if start_index == -1:
            break

        start = start_index + len(title1)
        end_index = content.find(title2, start)
        if end_index != -1:
            positions.append((start, end_index))
            index = end_index
        else:
            break

        index += 1

    mda_sections = []
    for start, end in positions:
        section = content[start:end].strip()
        mda_sections.append(section)

    return mda_sections

file_path = r"C:\Users\19599\OneDrive\Desktop\20221103\3453\0001558370-22-016112.txt"
title1 = "ITEM 2.  MANAGEMENT&#8217;S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS"
title2 = "ITEM 3.  QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK"

mda_sections = extract_mda_section(file_path, title1, title2)

# Translate the html texts into sentences
from bs4 import BeautifulSoup
import re

file_path = r"C:\Users\19599\OneDrive\Desktop\20221103\3453\0001558370-22-016112.txt"
title1 = "ITEM 2.  MANAGEMENT&#8217;S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS"
title2 = "ITEM 3.  QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK"

mda_sections = extract_mda_section(file_path, title1, title2)

# Read the content of the file
with open(file_path, 'r') as file:
    content = file.read()

# Pattern to match the MD&A section, same as used above
pattern = r"(?i)\bitem\s*2\b.*?(?=\bitem\s*\d+\b|\Z)"

# Find the MD&A section in the content
mda_sections = re.search(pattern, content, re.DOTALL)

if mda_sections:
    # Extract the matched section
    mda_html = mda_sections.group(0)

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(mda_html, 'html.parser')

    # Extract the plain text without HTML tags
    mda_text = soup.get_text()
    print(mda_text)
else:
    print("MD&A section not found in the HTML file")

# Clean mda_text
# Read the content of the file
with open(file_path, 'r') as file:
    content = file.read()

# Pattern to match the MD&A section, same as used above
pattern = r"(?i)\bitem\s*2\b.*?(?=\bitem\s*\d+\b|\Z)"

# Find the MD&A section in the content
mda_sections = re.search(pattern, content, re.DOTALL)

if mda_sections:
    # Extract the matched section
    mda_html = mda_sections.group(0)

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(mda_html, 'html.parser')

    # Extract the plain text without HTML tags
    mda_text = soup.get_text()

    # Replace non-breaking spaces with regular spaces
    mda_text = mda_text.replace(u'\xa0', u' ')

    # Remove leading/trailing whitespaces
    mda_text = mda_text.strip()

    # Remove newline characters
    mda_text = mda_text.replace('\n', ' ')

    # Remove special characters or punctuation
    mda_text = re.sub(r'[^\w\s]', '', mda_text)

    # Remove tables from the text
    tables = soup.find_all('table')
    for table in tables:
        table.extract()

    print(mda_text)
else:
    print("MD&A section not found in the HTML file")


