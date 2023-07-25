# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 12:53:52 2023

@author: 19599
"""

# JC Function A
import os
import re

file_path = r"C:\Users\19599\OneDrive\Desktop\cccp\10-Q"
def extract_mda_text(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()

        # Extract CIK from the file name
        cik = os.path.splitext(os.path.basename(file_path))[0]

        # Extract company's basic information and filing type from the head of the file
        # Modify the regular expressions based on the actual format of the head section
        head_info = re.findall(r'Company Name: (.+?)\n', file_content)
        filing_type = re.findall(r'FORM (.+?) ', file_content)

        # Extract MD&A part text
        target_string_1 = "Discussion and Analysis of Financial Condition"
        start_index_1 = file_content.lower().find(target_string_1.lower())
        start_index_2 = file_content.lower().find(target_string_1.lower(), start_index_1 + 1)

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

        return cik, head_info, filing_type, extracted_text

    except Exception as e:
        print("Error occurred while extracting MD&A text:", str(e))

# JC Function B
from bs4 import BeautifulSoup

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
        print("Error occurred while cleaning extracted text:", str(e))
        
# JC Function C

def generate_sentiment_report(cleaned_text):
    try:
        # Perform sentiment analysis on the cleaned text
        # Replace this part with your sentiment analysis algorithm or library

        # For demonstration purposes, let's assume a simple rule-based algorithm
        sentiment_score = 0
        positive_keywords = ["good", "positive", "strong"]
        negative_keywords = ["bad", "negative", "weak"]

        for keyword in positive_keywords:
            if keyword in cleaned_text.lower():
                sentiment_score += 1

        for keyword in negative_keywords:
            if keyword in cleaned_text.lower():
                sentiment_score -= 1

        # Prepare the sentiment report
        sentiment_report = {
            "Sentiment_Score": sentiment_score,
            "Sentiment_Determination_Logic": "A simple rule-based approach: Count positive and negative keywords."
        }

        return sentiment_report

    except Exception as e:
        print("Error occurred while generating the sentiment report:", str(e))

if __name__ == "__main__":
    # Sample data: Replace this with your actual file paths and data
    file_path_q1 = r"C:\Users\19599\OneDrive\Desktop\cccp\10-Q\0001696411-17-000008.txt"
    file_path_q4 = r"C:\Users\19599\OneDrive\Desktop\cccp\10-Q\0001696411-22-000012.txt"

    # Function A: Extract the MD&A text and basic information for Q1 and Q4
    cik_q1, head_info_q1, filing_type_q1, extracted_text_q1 = extract_mda_text(file_path_q1)
    cik_q4, head_info_q4, filing_type_q4, extracted_text_q4 = extract_mda_text(file_path_q4)

    # Function B: Clean the extracted text for Q1 and Q4
    cleaned_text_q1 = clean_extracted_text(extracted_text_q1)
    cleaned_text_q4 = clean_extracted_text(extracted_text_q4)

    # Function C: Generate sentiment reports for Q1 and Q4
    sentiment_report_q1 = generate_sentiment_report(cleaned_text_q1)
    sentiment_report_q4 = generate_sentiment_report(cleaned_text_q4)

    # Display the sentiment reports
    print("Sentiment Report for Q1:")
    print(sentiment_report_q1)
    print("\nSentiment Report for Q4:")
    print(sentiment_report_q4)


