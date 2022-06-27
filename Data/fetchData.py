# Author: Arihan Srirangapatnam
# Date: 05/11/2022
# Purpose: Script to call DiscosWeb Database API for data

import requests
import time
import csv

#Variable Declaration
URL = 'https://discosweb.esoc.esa.int' #API URL
token = '' # Access token
#Column headers for Data
csv_col = ['cosparId', 'depth', 'diameter', 'height', 'mass', 'name', 'objectClass', 'satno', 'shape', 'span', 'vimpelId', 'width', 'xSectAvg', 'xSectMax', 'xSectMin']
csv_file = "objectData.csv" #CSV file
count = 1 #iterative

#do-while loop
while True:
    
    #call to API
    response = requests.get(
        f'{URL}/api/objects',
        headers={
            'Authorization': f'Bearer {token}',
            'DiscosWeb-Api-Version': '2',
        },
        params={
            #request parameters
            "page[size]": 100,
            "page[number]": count,
            'sort': '-mass',
        },
    )

    doc = response.json()
    if response.ok:
        print("Receiving data from page %d..." %count)
        
        #append to CSV file
        try:
            with open(csv_file, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_col)
                writer.writeheader()
                for x in range(0,100):
                    writer.writerow(doc['data'][x]['attributes'])
        except IOError:
            print("I/O error")
    else:
        #once received invalid response, terminate loop
        print("DONE")
        break
    #sleep call to stay within call limits
    time.sleep(0.5)
    count += 1
