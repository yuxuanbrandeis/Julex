## Importing Modules

from nltk.tokenize import  sent_tokenize
# Machine Learning modules used to prepare and measure text
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
import torch
import re
from bs4 import BeautifulSoup

## MDA EXTRACTION
def extract(file_name):

    
    file_path = file_name
    with open(file_path, 'r') as file:
        file_content = file.read()
    
    pattern = re.compile(r'\bDiscussion\s+and\s+Analysis\s+of\s+Financial\s+Condition[s]?\b', re.IGNORECASE | re.DOTALL)
    matches = re.finditer(pattern, file_content)
    indices = [match.start() for match in matches]
    
    if len(indices) >= 1:
        start_index_1 = indices[0]
        if len(indices) >= 2:
            start_index_2 = indices[1]
        else:
            start_index_2 = -1
    else:
        # Handle the case when no occurrence is found
        start_index_1 = -1
        start_index_2 = -1
    

    
    #target_string_1 = "Discussion and Analysis of Financial Condition"
    #start_index_1 = file_content.lower().find(target_string_1.lower())
    #
    #start_index_2 = file_content.lower().find(target_string_1.lower(), start_index_1+1)
    
    
    
    
    
    pattern = re.compile(r"Disclosure[s]? About Market Risk", re.IGNORECASE)
    
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
    if end_index_2==-1 and start_index_2==-1:
        extracted_text = file_content[start_index_1:end_index_1]
    else:
        extracted_text = file_content[start_index_2:end_index_2]
    
    # Print the extracted text
    #print(extracted_text)
    
    
    
    
    
    
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
    clean_string = ''.join(string.replace('\n', '.').replace('\u200b', ' ').replace('\xa0', ' ' ).replace('&nbsp;',' '))
    

    clean_string = re.sub(r"(?i)table of contents", "", clean_string)

    clean_string = re.sub(r"\bquantitative and qualitative\b", "", clean_string, flags=re.IGNORECASE).strip()
    
    clean_string= "Management's " + clean_string
    
    clean_string = re.sub(r"\s*(?:item\s*7a\.?|item\s*4\.?|item\s*3\.?|item\s*8\.?|item\s+7a\.?|item\s+4\.?|item\s+3\.?|item\s+8\.?)\s*$", "", clean_string, flags=re.IGNORECASE)
    
    clean_string =  re.sub(r"[•;]", ".", clean_string)
    
    clean_string =  re.sub(r'\s*\.\s*(\.\s*)*', '. ', clean_string)
    clean_string = clean_string.strip()
    return clean_string



## Sentiment Analysis

# Load the models
finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-fls',num_labels=3)

# Download the Pre-trained transformer used to process our raw text
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-fls')

nlp = pipeline("text-classification", model=finbert, tokenizer=tokenizer)


# Sentiment - Download the Pre-trained transformer used to process our raw text
sent_tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")

# Sentiment - Download the FinBert model used to process our transformed data
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

def evaluate(filings):
  

    management_section = filings

    # For this section, break it into individual sentences
    sentences = sent_tokenize(management_section)

    # Initialize our FLS container
    fls = []

    # Define the container to collect stats related to the sentiment scores
    # for all forward-looking statement
    sentiments = torch.Tensor([0,0,0])

    # Process each sentence, converting into tokens required by the FinBert model.
    for sentence in sentences:
        # FLS prediction
        #print(sentence)
        prediction = nlp(sentence, top_k=3)[0]['label']

        # Capture FLS statements
        if prediction.startswith("Specific") or prediction.startswith("Non"):
            fls.append(sentence)

            # Tokenize - The FinBert model requires tensor-based tokens as input. For any g    iven    
                    # sentence, I must ensure the length must does not exceed the models self-impo    sed l    imit.
            encoded_input = sent_tokenizer(sentence, return_tensors="pt", truncation=True)
       
            with torch.no_grad():
                # Run the sentence through the model...
                output = model(**encoded_input)

                # The prediction will be in the form of a probability
                fls_sentiment = torch.nn.functional.softmax(output.logits, dim=-1)

                # Tally the predictions for each sentence
                sentiments = sentiments+fls_sentiment

    # Record the percentage of FLS sentences
    fls_pct=(len(fls)/len(sentences)*100)

    # Record the resulting sentiment for 'FLS' sentences within this section
    sentiments = sentiments.divide(len(sentences))

    score = model.config.id2label[sentiments.argmax().item()]
    #print(f'Filing: contains {len(sentences)} sentences of which {len(fls)} are "FLS"  with a sentiment of: {sentiments} => {score}')
    


    return fls_pct, score

## Did not add the output of MDA as it is long
## The number in ouput is FLS percentage
## example 10-K:

MDA=extract('https://www.sec.gov/Archives/edgar/data/1326801/000132680122000018/0001326801-22-000018.txt')
evaluate(MDA)

(18.84422110552764, 'neutral')


## example 10-Q:

MDA=extract('https://www.sec.gov/Archives/edgar/data/1326801/000132680122000082/0001326801-22-000082.txt')
evaluate(MDA)

Output:(11.960132890365449, 'neutral')






