## PART A
import os
from bs4 import BeautifulSoup
import re

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
                        
            
            target_string_1 = "Discussion and Analysis of Financial Condition"
            start_index_1 = file_content.lower().find(target_string_1.lower())
            
            start_index_2 = file_content.lower().find(target_string_1.lower(), start_index_1+1)
            
            
            
            
            
            pattern = re.compile(r"and Qualitative Disclosure[s]? About Market Risk", re.IGNORECASE)
            
            matches = re.finditer(pattern, file_content)
            
            indices = [match.start() for match in matches]
            
            if len(indices) >= 1:
                end_index_1 = indices[0]
                if len(indices) >= 2:
                    end_index_2 = indices[1]
                else:
                    end_index_2 = -1
            else:
                # Handle the case when no occurrence is found
                end_index_1 = -1
                end_index_2 = -1

            
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
import re

file_path = '/Users/hasanallahyarov/Desktop/files/2022/QTR1/8858/0000008858-22-000010.txt'
with open(file_path, 'r') as file:
    file_content = file.read()


target_string_1 = "Discussion and Analysis of Financial Condition"
start_index_1 = file_content.lower().find(target_string_1.lower())

start_index_2 = file_content.lower().find(target_string_1.lower(), start_index_1+1)





pattern = re.compile(r"and Qualitative Disclosure[s]? About Market Risk", re.IGNORECASE)

matches = re.finditer(pattern, file_content)

indices = [match.start() for match in matches]

if len(indices) >= 1:
    end_index_1 = indices[0]
    if len(indices) >= 2:
        end_index_2 = indices[1]
    else:
        end_index_2 = -1
else:
    # Handle the case when no occurrence is found
    end_index_1 = -1
    end_index_2 = -1


if end_index_1 == -1:
    pattern = re.compile(r"Control[s]? and Procedure[s]?", re.IGNORECASE)

    matches = re.finditer(pattern, file_content)

    indices = [match.start() for match in matches]

    if len(indices) >= 1:
        end_index_1 = indices[0]
        if len(indices) >= 2:
            end_index_2 = indices[1]
        else:
            end_index_2 = -1
    else:
        # Handle the case when no occurrence is found
        end_index_1 = -1
        end_index_2 = -1


# Check if there are at least 2000 characters between the occurrences
if end_index_1 - start_index_1 > 2000:
    # Extract the text between the occurrences
    extracted_text = file_content[start_index_1:end_index_1]
else:
    extracted_text = file_content[start_index_2:end_index_2]

# Print the extracted text
#print(extracted_text)



from bs4 import BeautifulSoup

import re

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

# Define the regular expression pattern for style matching
pattern = re.compile(r'text-align\s*:\s*center', re.IGNORECASE)

# Find all elements with style attribute matching the pattern and remove them
elements = soup.find_all(lambda tag: tag.has_attr('style') and pattern.search(tag['style']))
for element in elements:
    element.extract()

# Get the modified HTML content
modified_html = str(soup)


soup = BeautifulSoup(modified_html, 'html.parser')
text = soup.get_text()



string = text
clean_string = ''.join(string.replace('\n', ' ').replace('\u200b', '.').replace('\xa0', '.').replace('&nbsp;',''))
print(clean_string)

# %%%
# 2nd Way, Clean whole document first then extracting

import re
from bs4 import BeautifulSoup
file_path = '/Users/hasanallahyarov/Desktop/files/2022/QTR1/8858/0000008858-22-000010.txt'
with open(file_path, 'r') as file:
    file_content = file.read()

# Find the start and end tags of HTML sections
start_tag = '<DOCUMENT>'
end_tag = '</DOCUMENT>'

# Initialize a list to store the extracted HTML sections
html_sections = []

# Find and extract all HTML sections
start_index = file_content.find(start_tag)
while start_index != -1:
    end_index = file_content.find(end_tag, start_index + len(start_tag))
    if end_index != -1:
        html_content = file_content[start_index:end_index + len(end_tag)]
        html_sections.append(html_content)
        start_index = file_content.find(start_tag, end_index + len(end_tag))
    else:
        # Handle the case where the end tag is not found
        break
combined_html = ''.join(html_sections)


html_text = combined_html
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

# Define the regular expression pattern for style matching
pattern = re.compile(r'text-align\s*:\s*center', re.IGNORECASE)

# Find all elements with style attribute matching the pattern and remove them
elements = soup.find_all(lambda tag: tag.has_attr('style') and pattern.search(tag['style']))
for element in elements:
    element.extract()

# Get the modified HTML content
modified_html = str(soup)


soup = BeautifulSoup(modified_html, 'html.parser')
text = soup.get_text()



string = text
clean_string = ''.join(string.replace('\n', ' ').replace('\u200b', '').replace('\xa0', '').replace('&nbsp;',''))


target_string_1 = "Discussion and Analysis of Financial Condition"
start_index_1 = clean_string.lower().find(target_string_1.lower())

start_index_2 = clean_string.lower().find(target_string_1.lower(), start_index_1+1)





pattern = re.compile(r"and Qualitative Disclosure[s]? About Market Risk", re.IGNORECASE)

matches = re.finditer(pattern, clean_string)

indices = [match.start() for match in matches]

if len(indices) >= 1:
    end_index_1 = indices[0]
    if len(indices) >= 2:
        end_index_2 = indices[1]
    else:
        end_index_2 = -1
else:
    # Handle the case when no occurrence is found
    end_index_1 = -1
    end_index_2 = -1




# Check if there are at least 2000 characters between the occurrences
if end_index_1 - start_index_1 > 1500:
    # Extract the text between the occurrences
    extracted_text = clean_string[start_index_1:end_index_1]
else:
    extracted_text = clean_string[start_index_2:end_index_2]

# Print the extracted text
print(extracted_text)

# %%%

