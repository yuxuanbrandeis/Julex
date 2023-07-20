This code helps to run multiple reports.

After running whole code, you need to run:

extract('path_to_directory')

It will save teh output to excel file, which will contain:

The Clean MDA PART, CIK, TICKER, TITLE, DOCUMENT TYPE(10-Q or 10-K), SENTIMENT SCORE, FLS_PERCENTAGE


An example of 'path_to_directory':

If the file for 2022 year, 2022-01-03 for CIK-1013237 is here:

/Users/hasanallahyarov/Desktop/2022/20220103/1013237/0001013237-22-000005.txt

The nested structure should be as shown above, then the below code will loop through whole 2022 folder.

extract('/Users/hasanallahyarov/Desktop/2022')
