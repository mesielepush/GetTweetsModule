import os
import datetime
import joblib
from time import sleep
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

def format_day(date):
    day = '0' + str(date.day) if len(str(date.day)) == 1 else str(date.day)
    month = '0' + str(date.month) if len(str(date.month)) == 1 else str(date.month)
    year = str(date.year)
    return '-'.join([year, month, day])

def form_url(since, until):
        return f'https://twitter.com/search?q=(from%3A{account})%20until%3A{until}%20since%3A{since}&src=typed_query'

def increment_day(date, i):
    return date + datetime.timedelta(days=i)

account = input('twitter user: ')
print('FROM: ')
from_year = input('from year: ')
from_month = input('from month: ')
from_day = input('from day: ')
start = datetime.datetime(int(from_year), int(from_month), int(from_day))
print(f'From {start}')
print('Until: ')
to_year = input('to year: ')
to_month = input('to month: ')
to_day = input('to day: ')
end = datetime.datetime(int(to_year), int(to_month), int(to_day))
print(f'From {end}')

days = (end - start).days + 1

options = Options()
options.add_argument('--disable-gpu')
options.headless = True
driver = webdriver.Chrome(options=options,executable_path=r'meta\chromedriver.exe')

ids = []
delay = 1

saves = [x for x in range(30000) if x%100 == 0][1:]
save_turn = 0

if not os.path.exists(f'database/{account}'):
    os.mkdir(f'database/{account}')

account_data = os.listdir(f'database/{account}')

if os.path.exists(f'database/{account}/{format_day(increment_day(end, 0))}_{account}.npy'):
    print('Account ids are already in the database')
    
if len(account_data) != 0:
    start_date = account_data[0][:10]
    start = datetime.datetime(int(start_date[:4]), int(start_date[5:7]), int(start_date[8:10]))
    days = (end - start).days + 1
    ids = np.load(f'database/{account}/{account_data[0]}').tolist()
    saves = [x for x in saves if x > len(ids)]
    
    
for day in range(days):
    
    d1 = format_day(increment_day(start, 0))
    d2 = format_day(increment_day(start, 1))
    url = form_url(d1, d2)
    driver.get(url)
    sleep(delay)
    found_tweets = driver.find_elements_by_xpath(f'//a[contains(@href,"/{account}/")]')
    
    increment = 0
    
    while len(found_tweets) >= increment:
        
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(delay)
        found_tweets = driver.find_elements_by_xpath(f'//a[contains(@href,"/{account}/")]')
        for tweet in found_tweets:
            try:
                if 'photo' not in tweet.get_attribute('href').split('/'):

                    ids.append(tweet.get_attribute('href').split('/')[-1])
            except StaleElementReferenceException as e:
                print('PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP', tweet)
        #os.system('cls')
        print(f'{d1} to {d2}: {len(found_tweets)} tweets found, {len(ids)} total')
        
        increment += 10

    if len(ids) > saves[save_turn]:
        numpy_ids = np.array(ids)
        file_name = d2+'_'+account
        account_data = os.listdir(f'database/{account}')
        if len(account_data) != 0:
            for file in account_data:
                os.remove(f'database/{account}/{file}')
        
        np.save(os.path.join(f'database/{account}',file_name), numpy_ids, allow_pickle=True, fix_imports=True)
        save_turn +=1
        
    start = increment_day(start, 1)
    
numpy_ids = np.array(ids)
file_name = format_day(increment_day(end, 0))+'_'+account+'.np'

np.save(os.path.join(f'database/{account}',file_name), numpy_ids, allow_pickle=True, fix_imports=True)