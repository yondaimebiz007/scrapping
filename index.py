import requests
import csv
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0'
}

data = []

for i in range(1, 3832):
    print(f'working on {i} page')
    url = f'https://ethereum.stackexchange.com/users?tab=reputation&page={i}&filter=all'
    response = requests.get(url, headers = headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            text = link.text

            must_contain = ['/users/']
            must_not_contain = ['/login', '/signup']
            contains_required = all(word in href for word in must_contain)
            not_contains_required = all(word not in href for word in must_not_contain)

            if contains_required and not_contains_required and text:
                cell = {"name": text, "url": f"https://ethereum.stackexchange.com{href}"}
                data.append(cell)

    else:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')

# Specify the CSV file name
filename = 'output.csv'

# Get the headers from the keys of the first dictionary
headers = data[0].keys()

# Write data to CSV
with open(filename, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)

print(f"Data exported to {filename}")