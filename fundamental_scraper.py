import requests
from bs4 import BeautifulSoup

def fundamental_scraper(stock_ticker):
    output =""
    url = f'https://www.screener.in/company/{stock_ticker}/consolidated/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        about = soup.find('div', class_='about')
        paragraphs = about.find_all('p') if about else []
        for p in paragraphs:
            output += " " + p.get_text(strip=True)
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
            output += " " + k + " " + v + "."
            # return p.get_text(strip=True), data
        # print(output)
        return output
    else:
        print("Failed to retrieve the webpage")


x = fundamental_scraper("HDFCBANK")
print(x)

