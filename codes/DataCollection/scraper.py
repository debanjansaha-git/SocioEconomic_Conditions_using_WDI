# Scrape World Bank Data
# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Send a GET request to the website and retrieve its HTML content
url = 'https://data.worldbank.org/indicator/?tab=featured'
response = requests.get(url)

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the section that contains the featured indicators
page = soup.find('div', {'class': 'overviewPage'})

# Extract the names and overviews of the featured indicators
indicator_items = []
for body in page.find_all('div', {'class': 'overviewArea body'}):
    for item in body.find_all('section', {'class': 'nav-item'}):
        topic = item.find('h3')
        catg = topic.get('id').replace('-', ' ').title()
        for elem in item.find_all('ul'):
            for a in elem.find_all('a', {'href': True}):
                item_dict = {
                    'category_name': catg,
                    'indicator': a['href'].split('/')[2].split('?')[0],
                    'indicator_text': a.text.strip(),
                }
                indicator_items.append(item_dict)

# Create a pandas dataframe from the indicator_items list
df = pd.DataFrame(indicator_items)

# Save the dataframe
df.to_csv('Data\WorldBankFeaturedIndicators.csv', index=False)