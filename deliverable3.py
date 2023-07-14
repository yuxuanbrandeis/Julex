def extract(root_dir, dataframe=None):
    import re
    from bs4 import BeautifulSoup
    import os
    import pandas as pd
    
    if dataframe is None:
        dataframe = pd.DataFrame(columns=['Directory', 'Value'])
    
    # Loop through each directory in the root directory
    for date_folder in os.listdir(root_dir):
        date_folder_path = os.path.join(root_dir, date_folder)

        # Skip non-directory files
        if not os.path.isdir(date_folder_path):
            continue

        # Loop through the company folders
        for company_folder in os.listdir(date_folder_path):
            company_folder_path = os.path.join(date_folder_path, company_folder)

            # Skip non-directory files
            if not os.path.isdir(company_folder_path):
                continue

            # Get the report file path
            report_files = [os.path.join(company_folder_path, file) for file in os.listdir(company_folder_path)]

            # Skip if no report file found
            for report_file in report_files:
                # Open and read the report file
                with open(report_file, 'r') as file:
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
                
                if end_index_1 - start_index_1 > 2500:
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
                
                clean_string = "Management's " + clean_string
                
                data = {'Directory': company_folder, 'Date': date_folder, 'Value': clean_string}
                dataframe = dataframe.append(data, ignore_index=True)
                dataframe.to_excel('output.xlsx', index=False)

    return dataframe


# %%% 

root_dir = '/Users/meredithfan/Desktop/Julex/October'
result = extract(root_dir)

output_file = 'Users/meredithfan/Desktop/output.xlsx'
result.to_excel(output_file, index=False)
