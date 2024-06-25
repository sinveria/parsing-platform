from selenium import webdriver
from bs4 import BeautifulSoup

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

base_url = 'https://hh.ru/search/resume'
page_number = 0
resume_count = 0

try:
    while resume_count < 200:
        url = f'{base_url}?page={page_number}'
        # print(f"Scanning {url}")
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        resumes = soup.find_all("h3", {"data-qa": "bloko-header-3"})

        if not resumes:
            break

        for resume in resumes:
            title_span = resume.find("span", {"class": "title--iPxTj4waPRTG9LgoOG4t"})
            if title_span:
                link = title_span.find("a", {"data-qa": "serp-item__title"})
                if link and "Подробнее" not in link.get_text() and "применяются рекомендательные технологии" not in link.get_text():
                    print(link.get_text().strip())
                    resume_count += 1
                    if resume_count >= 200:
                        break
        
        page_number += 1

finally:
    driver.quit()