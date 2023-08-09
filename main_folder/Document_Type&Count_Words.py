def document_type(file):
    x=file[:1000]
    if  "10-K" in x:
        y="10-K"
    elif "10-Q" in x:
        y="10-Q"
        
    return y


def count_words(input_string):
    # Remove leading and trailing whitespaces (optional)
    input_string = input_string.strip()

    # Split the string into words based on spaces (you can use other delimiters if needed)
    words_list = input_string.split()

    # Count the number of words in the list
    word_count = len(words_list)

    return word_count
