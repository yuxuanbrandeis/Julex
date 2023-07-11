import os

desktop_path = r"C:\Users\19599\OneDrive"

def extract_content_between_fields(folder_path, field1, field2):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding="utf-8") as txt_file:
                    file_contents = txt_file.read()
                    start_index = file_contents.find(field1) + len(field1)
                    end_index = file_contents.find(field2)
                    extracted_content = file_contents[start_index:end_index].strip()
                    print(extracted_content)

extract_content_between_fields(desktop_path, "item2", "item3")

from bs4 import BeautifulSoup
import re

# Pattern to match the MD&A section, Same thing as used on above
pattern = r"(?i)\bitem\s*2\b.*?(?=\bitem\s*\d+\b|\Z)"

# Find the MD&A section in the content
extracted_content = re.search(pattern, content, re.DOTALL)

if extracted_content:
    # Extract the matched section
    mda_html = extracted_content.group(0)

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(mda_html, 'html.parser')

    # Extract the plain text without HTML tags
    mda_text = soup.get_text()
    print(mda_text)
else:
    print("MD&A section not found in the HTML file")
