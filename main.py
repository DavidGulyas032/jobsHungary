from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime
import time
import pandas as pd
from openpyxl.workbook import Workbook

joblist = []
job_urls = []
def get_url(page):
    url = f'https://www.profession.hu/allasok/hajdu-bihar/{page},0,32'
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    return soup

def get_links(soup):
    cards = soup.find_all("div", class_='card-body')

    for card in cards:
        try:
            job_url = card.find("a").get("href")
        except:
            job_url = ''
        job_urls.append(job_url)


def save_urls():
    page = 1
    while True:
        if page <=32:
            c = get_url(page)
            get_links(c)
            page+=1
        else:
            break

def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    try:
        job_title = soup.find('h1',class_='mt-md-4 mt-lg-0').text.strip()
    except:
        job_title = " "
    try:
        company_name = soup.find('a',id='job_link_cname-link').text.strip()
    except:
        company_name = " "
    try:
        company_location = soup.find('h3',itemprop='addressLocality').text.strip()
    except:
        company_location = " "
    try:
        requirements = soup.find('div',class_='text--inline-block').text.strip()
    except:
        requirements = " "
    try:
        education_skills = soup.find('div',id='requirements').text.strip()
    except:
        education_skills = " "
    try:
        sector = soup.find('div',id = 'orientation').text.strip().replace('\n',' ')
    except:
        sector = " "
    try:
        salary = soup.find('div',class_='adv-cover-tags adv-cover-tags--salary').text.strip()
    except:
        salary = " "

    jobs = {
        'title' : job_title,
        'name' : company_name,
        'location' : company_location,
        'requirements' : education_skills,
        'language_req' : requirements,
        'sector': sector,
        'salary' : salary
    }
    joblist.append(jobs)
    data = pd.DataFrame(joblist)
    data.to_excel('sample_data.xlsx',sheet_name='sheet1',index=False)


def main():
    save_urls()
    for links in job_urls:
        get_data(links)
main()
print(len(joblist))
