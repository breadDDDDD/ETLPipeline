import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

headers = {
    'user_agent': (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetch(url):

  ''' Starting the session '''

  session = requests.Session()
  try:
      response = session.get(url, headers=headers)
      response.raise_for_status()
      return response.content
  except requests.exceptions.RequestException as e:
      print(f"error {url}: {e}")
      return None


def scrape_web(url, page=1, delay=2):

  ''' Scraping the webpage based on the elements '''

  data =[]
  page_current = page
  try:

    while True :
        
      if page_current == 1:
        page_url = url
      else:
        page_url = f"{url}/page{page_current}"
      
      print(f'page {page_url}')

      content = fetch(page_url)
      if content :
        soup = BeautifulSoup(content, 'html.parser')

        #per product
        sections = soup.find_all('div', class_ = 'collection-card')
        for section in sections:
          prod_details = section.find_all('div', class_='product-details')

          #per details
          for detail in prod_details:
            title_tag = section.find('h3', class_='product-title')
            title = title_tag.text if title_tag else 'Not Available'

            desc = section.find_all('p', style='font-size: 14px; color: #777;')
            ratings = desc[0].text.split(' ')[-3]
            colors = desc[1].text.split()[0]
            size = desc[2].text.split(': ')[-1]
            gender = desc[3].text.split(': ')[-1]

            #per prrice details
            price_detail = detail.find('div', class_='price-container')
            if price_detail:
                price = price_detail.find('span', class_='price').text
            else:
                price = 'Not Available'

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item = {
                'title' : title,
                'price' : price,
                'ratings' : ratings,
                'colors' : colors,
                'size' : size,
                'gender' : gender,
                'timestamp' : timestamp
            }
            data.append(item)

        #next page
        next = soup.find('li', class_='page-item next')
        if next:
          page_current += 1
          time.sleep(delay)
          
        else:
          break
      else:
        break
    return data

  except Exception as e:
    print(f"An error occurred: {e}")