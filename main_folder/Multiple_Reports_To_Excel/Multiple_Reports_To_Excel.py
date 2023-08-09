import re
from bs4 import BeautifulSoup
import os
import pandas as pd
import requests
import yfinance as yahooFinance


def extract(root_dir, dataframe=None):

    
    ## Tickers and CIKs
    # create request header
    headers = {'User-Agent': "hasanallahyarov@address.com"}

    # get all companies data
    companyTickers = requests.get(
        "https://www.sec.gov/files/company_tickers.json",
        headers=headers
        )






    # dictionary to dataframe
    companyData = pd.DataFrame.from_dict(companyTickers.json(),
                                         orient='index')
                    
    
    
    ## CLeaning
    if dataframe is None:
        dataframe = pd.DataFrame(columns=['cik_str', 'Filed_At','document_type','FLS_pct','Score','num_words','Value'])
        
    for dir_name in os.listdir(root_dir):
        dir_path = os.path.join(root_dir, dir_name)
    
    # Check if it is a directory
        if os.path.isdir(dir_path):
        
        # Loop through each subdirectory inside the current directory
            for sub_dir_name in os.listdir(dir_path):
                sub_dir_path = os.path.join(dir_path, sub_dir_name)
            
            # Check if it is a subdirectory
                if os.path.isdir(sub_dir_path):
                
                # Loop through each file in the subdirectory
                    for file_name in os.listdir(sub_dir_path):
                        file_path = os.path.join(sub_dir_path, file_name)
                    
                    # Check if the file is a .txt file
                        if file_name.endswith('.txt'):
                        
                        # Open the file and perform operations
                            with open(file_path, 'r',encoding='utf-8') as file:
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
                            
                            if end_index_2==-1 and start_index_2==-1 and start_index_1<end_index_1:                          
                                extracted_text = file_content[start_index_1:end_index_1]
                            elif start_index_2<end_index_2:
                                extracted_text = file_content[start_index_2:end_index_2]
                            else:
                                extracted_text=""
                            if start_index_1==-1:
                                extracted_text=''

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
                            
                            soup = BeautifulSoup(modified_html_text, 'html.parser')
                            text = soup.get_text()
                            
                            string = text
                            clean_string = ''.join(string.replace('\n', ' . ').replace('\u200b', ' ').replace('\xa0', ' ').replace('&nbsp;',' '))
                            
                            clean_string = re.sub(r"(?i)table of contents", "", clean_string)
                            clean_string = re.sub(r"\bquantitative and Qualitative\b", "", clean_string, flags=re.IGNORECASE).strip()
            
                            clean_string = re.sub(r"\s*(?:item\s*7a\.?|item\s*4\.?|item\s*3\.?|item\s*8\.?|item\s+7a\.?|item\s+4\.?|item\s+3\.?|item\s+8\.?)\s*$", "", clean_string, flags=re.IGNORECASE)
                            
                            clean_string = "Management's " + clean_string
                            
                            clean_string =  re.sub(r"[•;]", " . ", clean_string)
                            clean_string =  re.sub(r'\s*\.\s*(\.\s*)*', '. ', clean_string)
                            clean_string = clean_string.strip()
                            print(dir_name)
                            print(sub_dir_name)
                    
                            

                            ## Document Type   
                            doc=document_type(file_content)
                            
                            ## Sentiment Analysis
                            
                            fls_pct, score = evaluate(clean_string)
                            
                            num_words= count_words(clean_string)
                                    
                            ## Combining all to dataframe
                            data = {'cik_str': sub_dir_name,'Filed_At': dir_name, 'document_type': doc, 'FLS_pct': fls_pct, 'Score': score, 'num_words':num_words, 'Value': clean_string}
                            dataframe = dataframe.append(data, ignore_index=True)
                            #dataframe.to_excel('C:\\Users\\hasanallahyarov\\Desktop\\test.xlsx', index=False)
                            
                            
                                
    # Merge the dataframes based on CIK numbers
    dataframe['cik_str'] = dataframe['cik_str'].astype(str)
    companyData['cik_str'] = companyData['cik_str'].astype(str)
    merged_df = pd.merge(dataframe, companyData, on='cik_str', how='left')
    merged_df.to_excel('C:\\Users\\hasanallahyarov\\Desktop\\result.xlsx', index=False)
            
    return merged_df
                            




            
# %%% Document Type


def document_type(file):
    x=file[:1000]
    if  "10-K" in x:
        y="10-K"
    elif "10-Q" in x:
        y="10-Q"
        
    return y



# %%% Sentiment Analysis

from nltk.tokenize import  sent_tokenize
# Machine Learning modules used to prepare and measure text
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
import torch

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
    
    for sentence in sentences:
        inputs = tokenizer(sentence, return_tensors="pt")
        tensor = inputs.input_ids.size()[1] 
        if tensor>512:
            x=len(sentence)//2
            new_sentence_1=sentence[:x]
            new_sentence_2=sentence[x:]
            sentences.remove(sentence)
            sentences.append(new_sentence_1)
            sentences.append(new_sentence_2)
            
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


# %%%

def count_words(input_string):
    # Remove leading and trailing whitespaces (optional)
    input_string = input_string.strip()

    # Split the string into words based on spaces (you can use other delimiters if needed)
    words_list = input_string.split()

    # Count the number of words in the list
    word_count = len(words_list)

    return word_count


# %%% Getting Prices




df = pd.read_excel('C:\\Users\\hasanallahyarov\\Desktop\\result.xlsx')



# Convert the 'Filed_At' column to datetime format
df['Filed_At'] = pd.to_datetime(df['Filed_At'], format='%Y%m%d')

# Convert the datetime format back to the desired format "YYYY-MM-DD"
df['Filed_At'] = df['Filed_At'].dt.strftime('%Y-%m-%d')
df['Price'] = None  
df['Price+1'] = None


for i in df.index:
    print(i)
    ticker=df['ticker'].iloc[i]
    
    if pd.notna(ticker):
        GetInformation = yahooFinance.Ticker(ticker)
    else:
        continue

    pd.set_option('display.max_rows', None)

    prices = GetInformation.history(period="max")
    
 
    
    prices.reset_index(inplace=True)
    
    prices['Date'] = pd.to_datetime(prices['Date'])
    
    prices['Date'] = prices['Date'].dt.strftime('%Y-%m-%d')
    
    desired_date = df['Filed_At'].iloc[i]
    
    
    result_df = prices[prices['Date'] == desired_date]
    
    if not result_df.empty:
        index_of_date = result_df.index[0]
    else:
        continue
    
    price_of_day = prices['Close'].iloc[index_of_date]
    
    price_of_next_day = prices['Close'].iloc[index_of_date+1]
    
    df.at[i, 'Price'] = price_of_day
    
    df.at[i, 'Price+1'] = price_of_next_day
    
df.to_excel('C:\\Users\\hasanallahyarov\\Desktop\\result_with_prices.xlsx', index=False)
    
    
    
# %%%
    
df = pd.read_excel('C:\\Users\\hasanallahyarov\\Desktop\\result_with_prices.xlsx')

df['Percentage_Diff'] = ((df['Price+1'] - df['Price']) / df['Price']) * 100

# Round the percentage difference to 2 decimal places
df['Percentage_Diff'] = df['Percentage_Diff'].round(2)

df.drop(['cik_str', 'FLS_pct', 'Score', 'Value', 'Date', 'title', 'Price', 'Price+1' ], axis=1, inplace=True)

df=df.dropna()

df = df[(df['num_words'] >= 1000) & (df['num_words'] <= 20000)]


import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


# Convert the Filed_At column to the year
df['Filed_At'] = pd.to_datetime(df['Filed_At'])

# Create separate columns for each day using one-hot encoding
df = pd.get_dummies(df, columns=['Filed_At'], prefix='day', drop_first=False)

# Create dummy variables for ticker and document_type
df = pd.get_dummies(df, columns=['ticker', 'document_type'], drop_first=True)

# Split the data into training and testing sets
X = df.drop('Percentage_Diff', axis=1)
y = df['Percentage_Diff']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the linear regression model with fixed effects
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r_squared = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r_squared}")

# Inspect coefficients and intercept
coefficients = pd.Series(model.coef_, index=X.columns)
intercept = model.intercept_

print("Coefficients:")
print(coefficients)
print("Intercept:")
print(intercept)
    
