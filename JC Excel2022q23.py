# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 22:42:30 2023

@author: 19599
"""

import os
import re
import pandas as pd
from bs4 import BeautifulSoup

def extract_file_data(file_path):
    # Open the file and read its content
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Extract necessary information from the file content
    date = re.search(r'FILED AS OF DATE:\s*(\d+)', file_content)
    date = date.group(1) if date else 'N/A'

    document_type = re.search(r'CONFORMED SUBMISSION TYPE:\s*(\w+)', file_content)
    document_type = document_type.group(1) if document_type else 'N/A'

    title = f'{document_type} {date}'

    cik_str = re.search(r'CENTRAL INDEX KEY:\s*(\d+)', file_content)
    cik_str = cik_str.group(1) if cik_str else 'N/A'

    # Extract and clean the MDA text
    mda_clean_text = extract_mda(file_content)
    if mda_clean_text is not None:
        mda_clean_text = clean_extracted_text(mda_clean_text)
    else:
        mda_clean_text = ''

    return date, document_type, title, cik_str, mda_clean_text

def extract_mda(file_content):
    # Find the indices of the MDA section in the file content
    target_string_1 = "Discussion and Analysis of Financial Condition"
    start_index_1 = file_content.lower().find(target_string_1.lower())
    start_index_2 = file_content.lower().find(target_string_1.lower(), start_index_1 + 1)

    end_index_1 = -1
    end_index_2 = -1

    pattern = re.compile(r"and Qualitative Disclosure[s]? About Market Risk", re.IGNORECASE)
    matches = re.finditer(pattern, file_content)
    indices = [match.start() for match in matches]

    if len(indices) >= 1:
        end_index_1 = indices[0]
        if len(indices) >= 2:
            end_index_2 = indices[1]

    if end_index_1 == -1:
        pattern = re.compile(r"Control[s]? and Procedure[s]?", re.IGNORECASE)
        matches = re.finditer(pattern, file_content)
        indices = [match.start() for match in matches]

        if len(indices) >= 1:
            end_index_1 = indices[0]
            if len(indices) >= 2:
                end_index_2 = indices[1]

    # Extract the MDA section from the file content
    if end_index_1 - start_index_1 > 2000:
        extracted_text = file_content[start_index_1:end_index_1]
    else:
        extracted_text = file_content[start_index_2:end_index_2]

    return extracted_text

def clean_extracted_text(extracted_text):
    try:
        # Parse the extracted text as HTML
        soup = BeautifulSoup(extracted_text, 'html.parser')

        # Remove specific tags that are not relevant
        tags_to_remove = ["span", "font"]
        for tag in tags_to_remove:
            for elem in soup.find_all(tag):
                elem.extract()

        # Remove subheadings and join paragraphs under each subheading
        subheadings = soup.find_all(re.compile('^h[1-5]$'))  # Find all heading tags (h1-h6)
        for subheading in subheadings:
            # Find the next siblings until the next subheading
            paragraphs = []
            sibling = subheading.next_sibling
            while sibling and sibling.name not in subheadings:
                if sibling.name == "p":
                    paragraphs.append(sibling.get_text(strip=True))
                sibling = sibling.next_sibling

            # Join paragraphs under each subheading
            subheading.string = " ".join(paragraphs)

        # Get the modified text content
        text = soup.get_text()

        clean_string = ''.join(text.replace('\n', ' ').replace('\u200b', '').replace('\xa0', ''))
        return clean_string
    except Exception as e:
        print("Error occurred while parsing HTML:", str(e))
        return ''

# Define the root directory
root_dir = r"C:\Users\19599\OneDrive\Desktop\2022\QTR2"

# Create a DataFrame to store the file data
df = pd.DataFrame(columns=['date', 'document_type', 'title', 'cik_str', 'mda_clean_text'])

# Loop through each directory in the root directory
for dir_name in os.listdir(root_dir):
    dir_path = os.path.join(root_dir, dir_name)

    # Check if it is a directory
    if os.path.isdir(dir_path):
        # Loop through each file in the directory
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)

            # Extract the necessary data from the file
            file_data = extract_file_data(file_path)

            # Append the file data to the DataFrame
            df = df.append(pd.Series(file_data, index=df.columns), ignore_index=True)

# Write the DataFrame to an Excel file
df.to_excel('MDA_Text_Q2.xlsx', index=False)

