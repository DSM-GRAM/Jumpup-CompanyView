from bs4 import BeautifulSoup as Soup
from selenium import webdriver

from db.models.company import RocketPunchModel

_BASE = 'https://www.rocketpunch.com/jobs?job=sw-developer&page={0}'
_COMPANY_BASE = 'https://www.rocketpunch.com{0}'


def parse():
    RocketPunchModel.drop_collection()

    browser = webdriver.Chrome('C:/Users/dmdkz/Desktop/chromedriver')
    browser.implicitly_wait(10)

    for page in range(1, 60):
        browser.get(_BASE.format(page))
        soup = Soup(browser.page_source, 'html.parser')

        for company_item in soup.select('div.company.item'):
            browser.get(_COMPANY_BASE.format(company_item.div.a['href']))
            soup = Soup(browser.page_source, 'html.parser')
            print(soup.find('h2', {'class': 'name'}).get_text())


if __name__ == '__main__':
    parse()
