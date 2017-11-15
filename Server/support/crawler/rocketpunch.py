from bs4 import BeautifulSoup as Soup
from selenium import webdriver
import re
import time

from db.models.company import RocketPunchModel, PositionEmbeddedModel

_BASE = 'https://www.rocketpunch.com/jobs?job=sw-developer&page={0}'
_COMPANY_BASE = 'https://www.rocketpunch.com{0}'


def parse():
    RocketPunchModel.objects.delete()

    browser = webdriver.Chrome('C:/Users/dmdkz/Desktop/chromedriver')
    browser.implicitly_wait(10)

    for page in range(1, 60):
        browser.get(_BASE.format(page))
        time.sleep(1)
        # 네트워크 속도 문제로 full load 실패 시 발생될 잠재적 문제 방어
        soup = Soup(browser.page_source, 'html.parser')

        for company_item in soup.select_one('div#company-list').select('div.company.item'):
            browser.get(_COMPANY_BASE.format(company_item.div.a['href']))
            time.sleep(1)
            # 네트워크 속도 문제로 full load 실패 시 발생될 잠재적 문제 방어
            soup = Soup(browser.page_source, 'html.parser')

            # --- Parse Basic Information
            name = soup.select('a.section')[2].get_text()
            image_url = soup.select_one('div.cover')['style'][22:-3]
            logo_url = soup.select_one('img.ui.image')['src']

            info = soup.select_one('section#company-intro').div.div.div.get_text()

            # --- Parse Company Information
            company_infos = soup.select_one('section#company-info').div.div.select('div.item')
            establish = None
            member_count = None
            address = None
            # email = None

            for company_info in company_infos:
                if '설립일' in company_info.get_text():
                    establish = re.search('\d+-\d+-\d+', company_info.get_text()).group()
                elif '구성원' in company_info.get_text():
                    member_count = re.search('\d+-\d+명', company_info.get_text()).group()
                elif '사무실' in company_info.get_text():
                    address = company_info.get_text().split('          ')[-1].strip()
                # elif '이메일' in company_info.get_text():
                #     email = re.search('\w+@.+', company_info.get_text()).group()

            # --- Parse Tags
            tags = [tag.get_text() for tag in soup.select_one('div.ui.bottom.attached.company.tag.segment').select('a')]

            # --- Parse Positions
            position_items = soup.select('div.small-job-card.item')
            positions = []

            for position_item in position_items:
                position_name = position_item.select_one('a.ui.primary.link')
                position_info = position_item.select_one('p.nowrap.job-stat-info')
                tech_stack = position_item.select_one('p.nowrap.job-specialties')

                positions.append(PositionEmbeddedModel(
                    position_name=position_name.get_text() if position_name else None,
                    position_info=position_info.get_text().strip() if position_info else None,
                    tech_stack=tech_stack.get_text().strip() if tech_stack else None))

            RocketPunchModel(
                name=name,
                image_url=image_url,
                logo_url=logo_url,
                info=info,
                establish=establish,
                member_count=member_count,
                address=address,
                # email=email,
                tags=tags,
                positions=positions).save()

            print('[RocketPunch] Parse Success : {0}'.format(name))

if __name__ == '__main__':
    parse()
