import re
from bs4 import BeautifulSoup
    
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
    return clean_string
    
    

