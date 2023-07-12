# Julex
## This is a collaborative space for Julex project involving code, instruction and descriptions. Individual work will be demonstrated

Respond to Yeabin's email :

We use modified code, in this function, we returned the list of a which is the extracted text from all the loop throughed MD&A report. The _name_ =="main" block return

def extract_text_from_files(root_dir):
    a = []

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
                    # Handle the case when no occurrence is found
                    end_index_1 = -1
                    end_index_2 = -1

                # Check if there are at least 2000 characters between the occurrences
                if end_index_1 - start_index_1 > 2000:
                    # Extract the text between the occurrences
                    extracted_text = file_content[start_index_1:end_index_1]
                else:
                    extracted_text = file_content[start_index_2:end_index_2]

                # Clean the extracted text
                cleaned_text = clean_extracted_text(extracted_text)
                if cleaned_text is not None:
                    a.append(cleaned_text)

    return a
#here is the main block to test the result with the HTML involved MD&A text 

if __name__ == "__main__":
    # Prompt the user to input the root directory path
    root_dir = input("Enter the root directory path: ")

    # Call the extract_text_from_files() function with the provided input
    extracted_text_list = extract_text_from_files(root_dir)

    # Print the extracted text
    for extracted_text in extracted_text_list:
        print(extracted_text)

