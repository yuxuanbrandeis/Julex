# 20221103-3453

import re #use regular expression to scrape the MD&A

file_path =  r"C:\Users\19599\OneDrive\Desktop\20221103\3453\0001558370-22-016112.txt"
with open(file_path, 'r') as file:
    content = file.read()

# Use regular expressions to extract the MD&A section based on a section heading pattern,
mda_match = re.search(r"(?i)\bitem\s*2\b.*?(?=\bitem\s*\d+\b|\Z)", content, re.DOTALL) #since this is 10-Q I use the sea
if mda_match:
    mda_text = mda_match.group()
    # Optionally, you can further process the extracted MD&A text

    # Print or use the extracted MD&A text
    print(mda_text)
else:
    print("MD&A section not found in the file")
    
from bs4 import BeautifulSoup

# Pattern to match the MD&A section, Same thing as used on above
pattern = r"(?i)\bitem\s*2\b.*?(?=\bitem\s*\d+\b|\Z)"

# Find the MD&A section in the content
mda_section = re.search(pattern, content, re.DOTALL)

if mda_section:
    # Extract the matched section
    mda_html = mda_section.group(0)

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(mda_html, 'html.parser')

    # Extract the plain text without HTML tags
    mda_text = soup.get_text()
    print(mda_text)
else:
    print("MD&A section not found in the HTML file")

# Cleanning mda_text
import string   
string_with_nbsp = mda_text   # Assuming `mda_text` contains the original string

# Step 1: Replace non-breaking spaces
formatted_string = mda_text.replace('\xa0', ' ')

# Step 2: Remove leading/trailing whitespaces
formatted_string = formatted_string.strip()

# Step 3: Remove newline characters
formatted_string = formatted_string.replace('\n', '')

# Step 4: Remove special characters or punctuation
formatted_string = formatted_string.translate(str.maketrans('', '', string.punctuation))

print(formatted_string)


