from selenium import webdriver

_BASE = 'https://www.rocketpunch.com/jobs?job=sw-developer&page={0}'
_PARSE_COUNT = 1


def parse():
    for i in range(1, _PARSE_COUNT + 1):
        browser = webdriver.Chrome()
        browser.get(_BASE.format(i))


if __name__ == '__main__':
    parse()
