import requests
from bs4 import BeautifulSoup

ticker = "HDFC BANK"
url = f'https://www.screener.in/company/{ticker}/consolidated/'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    about = soup.find('div', class_='about')
    
    # paragraphs = about.find_all('p') if about else []
    # for p in paragraphs:
    #     print(p.get_text(strip=True))

    p = about.find('p')
    print(p.get_text(strip=True))

    ratios = soup.find('div', class_='company-ratios')
    data = {}

    for li in ratios.find('ul', id='top-ratios').find_all('li'):
        name = li.find('span', class_='name').text.strip()
        value = li.find('span', class_='value').text.strip()
        data[name] = value

    del(data['Face Value'])

    for key, value in data.items():
        print(f"{key}:{value}")

else:
    print("Failed to retrieve the webpage")
