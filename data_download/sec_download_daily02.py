from datetime import date
import secedgar
import time
import pandas as pd
import os

def get_all_files_paths(root_dir): ## by Google Bard!
  """
  Get all files paths in subfolders.

  Args:
    root_dir: The root directory to start from.

  Returns:
    A list of all files paths.
  """

  all_files_paths = []
  for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
      file_path = os.path.join(dirpath, filename)
      all_files_paths.append(file_path)

  return(all_files_paths)

def daily_download(year, month, day, chunksize, path, email):
  # chunksize: how many files to download at one time, recommend 10
  # path: where to save files

  PATH = '{0}/{1}'.format(path, year*10000+month*100+day) # daily subfolder PATH
  
  downloaded = [] ## urls list already downloaded
  if os.path.exists(PATH):
    files = get_all_files_paths(PATH)
    downloaded = ['http://www.sec.gov/Archives/edgar/data'+file.replace(PATH, '').replace('\\', '/') for file in files]

  # saves only 10-K and 10-Q filings
  limit_to_10k_10q = lambda f: f.form_type.lower() in ("10-k", "10-q")

  my_filings = secedgar.filings(start_date=date(year, month, day),
                                      end_date=date(year, month, day),
                                      user_agent=email,
                                      entry_filter=limit_to_10k_10q)
  
  # get all the urls
  if len(downloaded) == 0: ## first time download

    try:
      urls = [url for value in my_filings.get_urls().values() for url in value]
      urls.sort()
      df = pd.DataFrame(urls, columns=['urls'])
      df.to_csv('{0}/{1}.csv'.format(path, year*10000+month*100+day), index=False, lineterminator='\n')

    except secedgar.exceptions.EDGARQueryError:
      # empty? then return log information
      log = 'Year {0} month {1} day {2} NO DATA!!!\n\n'.format(year, month, day)
      flag = 1
      return(log, flag)
    
  else: ## if not first time, read local urls file
    df = pd.read_csv('{0}/{1}.csv'.format(path, year*10000+month*100+day))
    urls = df.urls.to_list()
    urls = [url for url in urls if url not in downloaded]
  
  if len(urls) == 0: ## have already downloaded everything
    log = 'Year {0} month {1} day {2} downloading finished\n\n'.format(year, month, day)
    flag = 1
    return(log, flag)

  # time
  start_time = time.time()
  
  # download
  for i in range((len(urls)-1) // chunksize+1):
    if i == 3: ## break after three chunks
      break
  
    # filenames universe, do not download too many at one time
    filenames = [url.replace('http://www.sec.gov/Archives/', '') for url in urls[(i*chunksize):((i+1)*chunksize)]]
    
    # only download files with filename in the above universe
    limit_to_files = lambda f: f.file_name in filenames

    my_filings = secedgar.filings(start_date=date(year, month, day),
                                    end_date=date(year, month, day),
                                    user_agent=email,
                                    entry_filter=limit_to_files)
                                    
    # save
    try:
      my_filings.save(path)
    except Exception as e:
      log = 'Year {0} month {1} day {2} has exceptions {3}\n',format(year, month, day, e.__class__.__name__)
      flag = 0
      time.sleep(30) # relax half minute
      return(log, flag)

    # sleep
    time.sleep(10)
    
  # time
  end_time = time.time()
  
  # return log information
  log = 'Year {0} month {1} day {2} takes time {3} minutes\n'.format(year, month, day, (end_time-start_time)/60)
  flag = 0
  return(log, flag)

# test
flag = 0
while flag < 1:
  log, flag = daily_download(2022, 2, 24, 10, './test2', 'bo.wang@julexcapital.com')
  with open('log.txt', 'a', encoding='utf-8', newline='\n') as f:
    f.write(log) # write log file

###########################################
# import calendar
# calendar.monthrange(year, month)[1]
# will return the last day of month
