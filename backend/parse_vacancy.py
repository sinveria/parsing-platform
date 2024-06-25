from selenium import webdriver
from bs4 import BeautifulSoup

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

base_url = 'https://hh.ru/search/vacancy'
page_number = 0
vacancy_count = 0

try:
    while vacancy_count < 200:
        url = f'{base_url}?page={page_number}'
        # print(f"Scanning {url}")
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        vacancies = soup.find_all("span", {"class": "vacancy-name--c1Lay3KouCl7XasYakLk serp-item__title-link"})
        
        if not vacancies:
            break

        for link in vacancies:
            if "Подробнее" in link.get_text() or "применяются рекомендательные технологии" in link.get_text():
                continue
            
            print(link.get_text().strip())
            vacancy_count += 1
            if vacancy_count >= 200:
                break
        
        page_number += 1

finally:
    driver.quit()