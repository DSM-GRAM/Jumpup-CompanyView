from bs4 import BeautifulSoup as Soup
from selenium import webdriver

_BASE = 'https://www.wanted.co.kr/company/{0}'
_PARSE_COUNT = 1000


def parse():
    for i in range(1, _PARSE_COUNT + 1):
        browser = webdriver.Chrome('C:/Users/dmdkz/Desktop/chromedriver')
        browser.implicitly_wait(10)

        browser.get(_BASE.format(i))
        soup = Soup(browser.page_source, 'html.parser')


if __name__ == '__main__':
    parse()
