
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

    # Process each sentence, converting into tokens required by the FinBert model.
    for sentence in sentences:
        # FLS prediction
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
    print(f'Filing: contains {len(sentences)} sentences of which {len(fls)} are "FLS"  with a sentiment of: {sentiments} => {score}')
    

# Add the measures to our results table
    return fls_pct, score
