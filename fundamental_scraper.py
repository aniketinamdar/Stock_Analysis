import requests
from bs4 import BeautifulSoup

# returns scraper_data, prompt_data 2 strings
def fundamental_scraper(stock_symbol):
    scraper_data =""
    prompt_data = ""
    url = f'https://www.screener.in/company/{stock_symbol}/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        about = soup.find('div', class_='about')
        paragraphs = about.find_all('p') if about else []
        for p in paragraphs:
            scraper_data += " " + p.get_text(strip=True)
        # p = about.find('p')
        # print(p.get_text(strip=True))
        ratios = soup.find('div', class_='company-ratios')
        data = {}
        for li in ratios.find('ul', id='top-ratios').find_all('li'):
            name = li.find('span', class_='name').text.strip()
            value = li.find('span', class_='value').text.strip()
            data[name] = value
        # del(data['Face Value'])
        data = {k: v.replace('\n', '').strip() for k, v in data.items()}
        data = {k: v.replace('        ', ' ').strip() for k, v in data.items()}
        data = {k: v.replace('   ', ' ').strip() for k, v in data.items()}
        data = {k: v.replace('Cr.', 'Cr').strip() for k, v in data.items()}
        # print(output)
        for k,v in data.items():
            prompt_data += " " + k + " " + v + "."
            # return p.get_text(strip=True), data
        # print(output)
        return scraper_data, prompt_data
    else:
        print("Failed to retrieve the webpage")

# fundamental_scraper("HDFCBANK")

