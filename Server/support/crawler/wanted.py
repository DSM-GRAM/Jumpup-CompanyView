from bs4 import BeautifulSoup as Soup
from selenium import webdriver

from db.models.company import WantedModel

_BASE = 'https://www.wanted.co.kr/company/{0}'
_PARSE_COUNT = 300


def parse():
    WantedModel.objects.delete()

    # browser = webdriver.Chrome('C:/Users/dmdkz/Desktop/chromedriver')
    # browser.implicitly_wait(10)
    # Ready Selenium

    for i in range(1, _PARSE_COUNT + 1):
        browser = webdriver.Chrome('C:/Users/dmdkz/Desktop/chromedriver')
        browser.implicitly_wait(10)
        # Ready Selenium

        browser.get(_BASE.format(i))
        soup = Soup(browser.page_source, 'html.parser')

        name = soup.select_one('div.company-header').h1.get_text()
        image_urls = soup.select('div.image')
        image_url = image_urls[0]['style'][22:-3] if len(image_urls) else None
        logo_url = soup.select_one('img.logo')['src']

        info = str(soup.find('span', {'data-reactid': '.0.1.1.0.2.0.2.0.$0'}))[41:-7].replace('<br/>', '\n')

        establish = soup.find('div', {'data-reactid': '.0.1.1.0.2.0.1.0.1.1'}).get_text()
        member_count = soup.find('div', {'data-reactid': '.0.1.1.0.2.0.1.0.2.1'}).get_text()
        label = soup.find('div', {'data-reactid': '.0.1.1.0.2.0.1.0.3.1'}).get_text()
        address = soup.find('div', {'data-reactid': '.0.1.1.0.2.0.1.1.0.1'}).get_text()

        positions = [position.h1.get_text() for position in soup.find_all('div', {'class': 'col-xs-10'})]

        WantedModel(
            name=name,
            image_url=image_url,
            logo_url=logo_url,
            info=info,
            establish=establish,
            member_count=member_count,
            label=label,
            address=address,
            positions=positions).save()

        browser.close()
        print('[Wanted] Parse Success : {0}'.format(name))

if __name__ == '__main__':
    parse()

