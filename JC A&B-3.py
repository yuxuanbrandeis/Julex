#JC Update
## PART A
import os
from bs4 import BeautifulSoup
import re
root_dir = '/Users/19599/OneDrive/Desktop/20221107'

def extract_files(root_dir):
    a = []
    cik_list = []

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

                # Extract CIK from the file name
                cik = os.path.splitext(file_name)[0]
                cik_list.append(cik)

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
                    end_index_1 = -1
                    end_index_2 = -1

                if end_index_1 - start_index_1 > 2000:
                    extracted_text = file_content[start_index_1:end_index_1]
                else:
                    extracted_text = file_content[start_index_2:end_index_2]

                a.append(extracted_text)

    return cik_list, a


def clean_extracted_text(extracted_text):
    try:
        soup = BeautifulSoup(extracted_text, 'html.parser')

        # Remove specific tags that are not relevant
        tags_to_remove = ["span", "font"]
        for tag in tags_to_remove:
            for elem in soup.find_all(tag):
                elem.extract()

        # Remove subheadings and join paragraphs under each subheading
        subheadings = soup.find_all(re.compile('^h[1-6]$'))  # Find all heading tags (h1-h6)
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


if __name__ == "__main__":
    # Example usage
    root_dir = '/Users/19599/OneDrive/Desktop/20221107'

    # Extract files and CIK list
    cik_list, extracted_files = extract_files(root_dir)

    # Clean extracted text
    cleaned_files = [clean_extracted_text(text) for text in extracted_files]

    # Print CIK list and cleaned files
    print("CIK List:", cik_list)
    print("Cleaned Files:", cleaned_files)

# PART B

def clean_extracted_text(extracted_text):
    try:
        soup = BeautifulSoup(extracted_text, 'html.parser')

        # Remove specific tags that are not relevant
        tags_to_remove = ["span", "font"]
        for tag in tags_to_remove:
            for elem in soup.find_all(tag):
                elem.extract()

        # Remove subheadings and join paragraphs under each subheading
        subheadings = soup.find_all(re.compile('^h[1-6]$'))  # Find all heading tags (h1-h6)
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

file_path = '/Users/19599/OneDrive/Desktop/20221104/1961/0001264931-22-000176.txt'
with open(file_path, 'r') as file:
    file_content = file.read()

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
    else:
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

if end_index_1 == -1:
    print("MDA not found in the file.")
else:
    if end_index_1 - start_index_1 > 2000:
        extracted_text = file_content[start_index_1:end_index_1]
    else:
        extracted_text = file_content[start_index_2:end_index_2]

    clean_string = clean_extracted_text(extracted_text)
    print("MDA Clean String:")
    print(clean_string)

