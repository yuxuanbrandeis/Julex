
def extract(root_dir, dataframe=None):
    import re
    from bs4 import BeautifulSoup
    import os
    import pandas as pd
    
    if dataframe is None:
        dataframe = pd.DataFrame(columns=['Directory', 'Value'])
    
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

                if end_index_2==-1 and start_index_2==-1:
                    extracted_text = file_content[start_index_1:end_index_1]
                elif end_index_1 - start_index_1 > 2500:
                    # Extract the text between the occurrences
                    extracted_text = file_content[start_index_1:end_index_1]
                else:
                    extracted_text = file_content[start_index_2:end_index_2]
                
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
                clean_string = ''.join(string.replace('\n', ' ').replace('\u200b', '.').replace('\xa0', '.').replace('&nbsp;',''))
                
                clean_string = re.sub(r"(?i)table of contents", "", clean_string)
                clean_string = re.sub(r"\bquantitative\b", "", clean_string, flags=re.IGNORECASE).strip()

                clean_string = re.sub(r"\s*(?:item\s*7a\.?|item\s*4\.?|item\s*3\.?|item\s*8\.?|item\s+7a\.?|item\s+4\.?|item\s+3\.?|item\s+8\.?)\s*$", "", clean_string, flags=re.IGNORECASE)
                
                clean_string = "Management's " + clean_string
                
                data = {'Directory': dir_name, 'Value': clean_string}
                dataframe = dataframe.append(data, ignore_index=True)
        dataframe.to_excel('output10.xlsx', index=False)

    return dataframe
                
