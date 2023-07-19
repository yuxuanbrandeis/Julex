import os
import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import string
import nltk
nltk.download('stopwords')

# Extracts the content of a file given its path
def extract_text_from_file(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
    return file_content

# Extracts the CIK (Central Index Key) from a given file name
def extract_cik_from_filename(file_name):
    cik = os.path.splitext(file_name)[0]
    return cik

# Extracts the text within a specified section of the given content
def extract_text_sections(file_content, start_phrase, end_phrase):
    start_index = file_content.lower().find(start_phrase.lower())
    end_index = -1
    pattern = re.compile(end_phrase, re.IGNORECASE)
    matches = re.finditer(pattern, file_content)
    indices = [match.start() for match in matches]
    if len(indices) >= 1:
        end_index = indices[0]
    return file_content[start_index:end_index]

# Cleans the extracted text by converting to lower case, removing punctuation, numbers and stop words
def clean_text(text):
    # Additional cleaning steps
    text = text.lower()  # Convert text to lowercase
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    text = re.sub(r'\d+', '', text)  # Remove numbers
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [word for word in words if word not in stop_words]  # Remove stop words
    clean_string = ' '.join(words)
    clean_string = clean_string.replace('\n', ' ').replace('\u200b', '').replace('\xa0', '')  # Replace newline and other characters
    return clean_string

# Processes all files in a directory by extracting and cleaning text
def process_files_in_directory(root_dir):
    extracted_texts = []
    cik_list = []
    
    # Loop through each directory in the root directory
    for dir_name in os.listdir(root_dir):
        dir_path = os.path.join(root_dir, dir_name)

        # Check if it is a directory
        if os.path.isdir(dir_path):
            # Loop through each sub-directory in the directory
            for sub_dir_name in os.listdir(dir_path):
                sub_dir_path = os.path.join(dir_path, sub_dir_name)
                
                if os.path.isdir(sub_dir_path):
                    # Loop through each file in the sub-directory
                    for file_name in os.listdir(sub_dir_path):
                        file_path = os.path.join(sub_dir_path, file_name)

                        # Make sure it's a file, not a directory
                        if os.path.isfile(file_path):
                            file_content = extract_text_from_file(file_path)
                            cik = extract_cik_from_filename(file_name)
                            cik_list.append(cik)
                            extracted_text = extract_text_sections(file_content, "Discussion and Analysis of Financial Condition", "and Qualitative Disclosure[s]? About Market Risk")
                            cleaned_text = clean_text(extracted_text)
                            extracted_texts.append(cleaned_text)

    return cik_list, extracted_texts

# Main function
if __name__ == "__main__":
    root_dir = r'C:\Users\19599\OneDrive\Desktop\2020_10K'
    cik_list, cleaned_files = process_files_in_directory(root_dir)
    #print("CIK List:", cik_list)
    #print("Cleaned Files:", cleaned_files)

    # Loop through the cleaned_files list and print each item
    for text in cleaned_files:
        print(text)