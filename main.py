import requests
import bs4
from fake_headers import Headers
import json

def get_url():
    headers = Headers(browser="firefox", os='win')
    headers_data = headers.generate()
    url = 'https://spb.hh.ru/search/vacancy'
    params = {'text': ('Python', 'Django', 'Flask'),
              'area': ('1', '2')}
    main_html = requests.get(url=url, params=params, headers=headers_data).text
    soup = bs4.BeautifulSoup(main_html, "lxml")

    return soup


def get_vacancies(soup):
    vacancies = []
    items = soup.find_all('div', class_='vacancy-card--z_UXteNo7bRGzxWVcL7y')
    for item in items:
        link = item.find('a', class_='bloko-link')['href']
        salary = item.find('span', class_='bloko-text').text
        company = item.find('a', class_="bloko-link bloko-link_kind-secondary").text
        city = item.find("span", {"data-qa":"vacancy-serp__vacancy-address"}).text
        if salary == company:
            salary = 'Не указана'

        vacancies.append({
                'link': link,
                'salary': salary,
                'company': company,
                'city': city,      
            })
        
    return vacancies


def create_json(vacancies):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(vacancies, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    soup = get_url()
    vacancies = get_vacancies(soup)
    create_json(vacancies)