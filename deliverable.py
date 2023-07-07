def extract(file_name):
    import re
    from bs4 import BeautifulSoup
    
    file_path = file_name
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
    
    
    # Check if there are at least 2000 characters between the occurrences
    if end_index_1 - start_index_1 > 2000:
        # Extract the text between the occurrences
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
    clean_string = ''.join(string.replace('\n', ' ').replace('\u200b', '.').replace('\xa0', '.').replace('&nbsp;',''))
    print(clean_string)
    
## EXAMPLE:
extract('/Users/hasanallahyarov/Desktop/files/2022/QTR1/8858/0000008858-22-000010.txt')
