from bs4 import BeautifulSoup as Soup
from selenium import webdriver
import re

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

        for company_item in soup.select_one('div#company-list').select('div.company.item'):
            # From div#company-list, select div.company.item
            browser.get(_COMPANY_BASE.format(company_item.div.a['href']))
            soup = Soup(browser.page_source, 'html.parser')

            name = soup.select('a.section')[2].get_text()
            image_url = soup.select_one('div.cover')['style'][22:-3]
            logo_url = soup.select_one('img.ui.image')['src']

            info = soup.select_one('section#company-intro').div.div.div.get_text()



if __name__ == '__main__':
    parse()
