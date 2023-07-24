def extract(root_dir, dataframe=None):
    import re
    from bs4 import BeautifulSoup
    import os
    import pandas as pd
    import requests

    
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
                            data = {'cik_str': sub_dir_name,'Filed_At': dir_name, 'document_type': doc, 'FLS_pct':fls_pct, 'Score':score, 'num_words':num_words, 'Value': clean_string}
                            dataframe = dataframe.append(data, ignore_index=True)
                            
                            
                            
                                
                    # Merge the dataframes based on CIK numbers
                    dataframe['cik_str'] = dataframe['cik_str'].astype(str)
                    companyData['cik_str'] = companyData['cik_str'].astype(str)
                    merged_df = pd.merge(dataframe, companyData, on='cik_str', how='left')
                    merged_df.to_excel('output13.xlsx', index=False)
            
    return merged_df
                          
