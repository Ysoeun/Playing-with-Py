#기사 썸네일을 포함해서 크롤링하기

from bs4 import BeautifulSoup
from selenium import webdriver

from openpyxl import Workbook

driver = webdriver.Chrome('chromedriver')

url = "https://bit.ly/30nrK7M" #url 길어서 줄임

driver.get(url)
req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')

wb = Workbook()
ws1 = wb.active
ws1.title = "articles"
ws1.append(["제목", "링크", "신문사", "썸네일"])

articles = soup.select('#main_pack > div.news.mynews.section._prs_nws > ul > li')

for article in articles:
    a_tag = article.select_one('dl > dt > a')

    title = a_tag.text
    url = a_tag['href']
    comp = article.select_one('dd.txt_inline > span._sp_each_source').text.split(' ')[0].replace('언론사','')
    thumbnail = article.select_one('img')['src']

    ws1.append([title, url, comp, thumbnail])

driver.quit()
wb.save(filename='articles.xlsx')

########################################
#나한테 메일보내기

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


# 보내는 사람 정보
me = "내지메일@gmail.com"
my_password = "비번"

# 로그인하기
s = smtplib.SMTP_SSL('smtp.gmail.com')
s.login(me, my_password)

# 받는 사람 정보
emails = ['네이버1@naver.com','네이버2@naver.com']

for you in emails:
    # 메일 기본 정보 설정
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "[공유]추석기사 더미"
    msg['From'] = me
    msg['To'] = you

# 메일 내용 쓰기
    content = "파이썬혼자놀기 2강 숙제"
    part2 = MIMEText(content, 'plain')
    msg.attach(part2)

    part = MIMEBase('application', "octet-stream")
    with open("articles.xlsx", 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment", filename="추석기사.xlsx")
    msg.attach(part)

# 메일 보내고 서버 끄기
    s.sendmail(me, you, msg.as_string())
s.quit()