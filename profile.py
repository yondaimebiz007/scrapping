import requests
import csv
from bs4 import BeautifulSoup
import re
import os

headers = {
    'User-Agent': 'Mozilla/5.0'
}

data = []

with open('output.csv', newline = '', encoding = 'utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)

    for i, row in enumerate(csvreader):

        print(f'working on {i}')
        url = row[1]
        print(f"url, {url}")
        response = requests.get(url, headers = headers)
        
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
                            
                    # if inner_div:

                    #     ul_elements = inner_div.find_all('ul')

                    #     for idx, ul in enumerate(ul_elements, start = 1):
                    #         # li_elements = ul.find('li')
                    #         # print(f"{li_elements.get_text()}")
                    #         print(f"UL #{idx}:")
                    #         print(f"{ul.get_text().strip()}")
                    #         # print(ul.prettify())  # or ul.get_text()

        else:
            print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
        
        data.append(cell)

        if i % 10 == 0:
            # Specify the CSV file name
            filename = 'update.csv'

            if os.path.exists(filename):
                with open(filename, 'r', newline='') as file:
                    reader = csv.reader(file)
                    updatedata = list(reader)
                updatedata.extend(data)

                with open(filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(updatedata)
            else:

                # Get the headers from the keys of the first dictionary
                headers = data[0].keys()

                # Write data to CSV
                with open(filename, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(data)

                print(f"Data exported to {filename}")


        if i >= 100:
            break