import requests
import csv
from bs4 import BeautifulSoup
import re
import os
import logging

requestheaders = {
    'User-Agent': 'Mozilla/5.0'
}

data = []

logging.basicConfig(
    filename='app.log',       # Log messages will be saved to this file
    level=logging.INFO,       # Set the minimum level of messages to log
    format='%(asctime)s - %(levelname)s - %(message)s'  # Message format
)

with open('output.csv', newline = '', encoding = 'utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)

    for i, row in enumerate(csvreader):

        print(f'working on {i}')
        url = row[1]
        response = requests.get(url, headers = requestheaders)
        cell = {"Name": row[0], "URL": row[1], "GitHub": row[2], "Twitter": row[3], "Website": row[4]}
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            parent_div = soup.find('div', id = 'mainbar-full')

            if parent_div:
                outer_div = parent_div.find('div')

                if outer_div:
                    inner_div = outer_div.find('div')
                    li_elements = inner_div.find_all('li')

                    for li in li_elements:
                        links = li.find_all('a')
                        for link in links:
                            href = link.get('href')
                            text = ''
                            anchor = link.find(class_ = 'v-visible-sr')

                            if anchor:
                                text = anchor.text
                            else:
                                text = "Website"
                            
                            cell[text] = href
                            
        else:
            print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
        
        data.append(cell)

        if i % 10 == 0:
            # Specify the CSV file name
            filename = 'update.csv'
            updatedata = []

            if os.path.exists(filename):
                with open(filename, 'r', newline='') as file:
                    reader = csv.reader(file)
                    updatedata = list(reader)

            updatedata.extend(data)
            fileheaders = data[0].keys()

            # Write data to CSV
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fileheaders)
                writer.writeheader()
                writer.writerows(data)

            print(f"Data exported to {filename}")
            logging.info(f'checked {i} items...')
