#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 14:56:59 2023

@author: hasanallahyarov
"""

## PART A
import os
from bs4 import BeautifulSoup

a=[]

# Define the root directory
root_dir = '/Users/hasanallahyarov/Desktop/files/2022/QTR1'

# Loop through each directory in the root directory
for dir_name in os.listdir(root_dir):
    dir_path = os.path.join(root_dir, dir_name)
    
    # Check if it is a directory
    if os.path.isdir(dir_path):
        # Loop through each file in the directory
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)
            
            # Open the file and perform operations
            with open(file_path, 'r') as file:
                file_content = file.read()
            
            target_string_1 = "Discussion and Analysis of Financial Condition and Results of Operations"
            start_index_1 = file_content.lower().find(target_string_1.lower())

            start_index_2 = file_content.lower().find(target_string_1.lower(), start_index_1+1)

            target_string_2 = "and Qualitative Disclosures About Market Risk"
            end_index_1 = file_content.lower().find(target_string_2.lower())

            end_index_2 = file_content.lower().find(target_string_2.lower(),end_index_1+1)

            # Find the indices of the first occurrence of "MDA"
            #start_index_1 = file_content.find("Discussion and Analysis of Financial Condition and Results of Operations")

            # Find the indices of the first occurrence of "ITEM3"
            #end_index_1 = file_content.find("Quantitative and Qualitative Disclosures About Market Risk")

            # Find the indices of the second occurrence of "MDA"
            #start_index_2 = file_content.find("Discussion and Analysis of Financial Condition and Results of Operations", start_index_1 + 1)

            # Find the indices of the second occurrence of "Item3" 
            #end_index_2 = file_content.find("Quantitative and Qualitative Disclosures About Market Risk", end_index_1 + 1)

            # Check if there are at least 2000 characters between the occurrences
            if end_index_1 - start_index_1 > 2000:
                # Extract the text between the occurrences
                extracted_text = file_content[start_index_1:end_index_1]
            else:
                extracted_text = file_content[start_index_2:end_index_2]
            
            a.append(extracted_text)
            
            
            
# %%% 

## PART B
list_for_MDA=[]
for i in a:
    try:
        
        html_text = i
        # Create a BeautifulSoup object
        soup = BeautifulSoup(html_text, 'html.parser')
        
        # Find all table tags
        tables = soup.find_all('table')
        
        # Remove the tables from the parsed structure
        for table in tables:
            table.decompose()
        
        # Get the modified HTML text without the tables
        modified_html_text = str(soup)
        # Extract the text content without HTML tags
        
        # Assuming the HTML content is stored in the variable 'html_text'
        soup = BeautifulSoup(modified_html_text, 'html.parser')
        
        # Find all elements with style attribute containing 'text-align:center' and remove them
        elements = soup.find_all(lambda tag: tag.has_attr('style') and 'text-align:center' in tag['style'])
        for element in elements:
            element.extract()
        
        # Get the modified HTML content
        modified_html = str(soup)


        soup = BeautifulSoup(modified_html, 'html.parser')
        text = soup.get_text()



        string = text
        clean_string = ''.join(string.replace('\n', ' ').replace('\u200b', '').replace('\xa0', ''))
        list_for_MDA.append(clean_string)

    except Exception as e:
        print("Error occurred while parsing HTML:", str(e))
        
        
# %%%

## FOR INDIVIDUAL ONE TO TRY

file_path = '/Users/hasanallahyarov/Desktop/files/2022/QTR1/320193/0000320193-22-000007.txt'
with open(file_path, 'r') as file:
    file_content = file.read()

target_string_1 = "Discussion and Analysis of Financial Condition and Results of Operations"
start_index_1 = file_content.lower().find(target_string_1.lower())

start_index_2 = file_content.lower().find(target_string_1.lower(), start_index_1+1)

target_string_2 = "and Qualitative Disclosures About Market Risk"
end_index_1 = file_content.lower().find(target_string_2.lower())

end_index_2 = file_content.lower().find(target_string_2.lower(),end_index_1+1)

# Find the indices of the first occurrence of "MDA"
#start_index_1 = file_content.find("Discussion and Analysis of Financial Condition and Results of Operations")

# Find the indices of the first occurrence of "ITEM3"
#end_index_1 = file_content.find("Quantitative and Qualitative Disclosures About Market Risk")

# Find the indices of the second occurrence of "MDA"
#start_index_2 = file_content.find("Discussion and Analysis of Financial Condition and Results of Operations", start_index_1 + 1)

# Find the indices of the second occurrence of "Item3" 
#end_index_2 = file_content.find("Quantitative and Qualitative Disclosures About Market Risk", end_index_1 + 1)

# Check if there are at least 2000 characters between the occurrences
if end_index_1 - start_index_1 > 2000:
    # Extract the text between the occurrences
    extracted_text = file_content[start_index_1:end_index_1]
else:
    extracted_text = file_content[start_index_2:end_index_2]

# Print the extracted text
#print(extracted_text)



from bs4 import BeautifulSoup



html_text = extracted_text
# Create a BeautifulSoup object
soup = BeautifulSoup(html_text, 'html.parser')

# Find all table tags
tables = soup.find_all('table')

# Remove the tables from the parsed structure
for table in tables:
    table.decompose()

# Get the modified HTML text without the tables
modified_html_text = str(soup)
# Extract the text content without HTML tags

# Assuming the HTML content is stored in the variable 'html_text'
soup = BeautifulSoup(modified_html_text, 'html.parser')

# Find all elements with style attribute containing 'text-align:center' and remove them
elements = soup.find_all(lambda tag: tag.has_attr('style') and 'text-align:center' in tag['style'])
for element in elements:
    element.extract()

# Get the modified HTML content
modified_html = str(soup)


soup = BeautifulSoup(modified_html, 'html.parser')
text = soup.get_text()



string = text
clean_string = ''.join(string.replace('\n', ' ').replace('\u200b', '').replace('\xa0', ''))
print(clean_string)


