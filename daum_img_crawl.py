import dload
from bs4 import BeautifulSoup
from selenium import webdriver
import time

driver = webdriver.Chrome('chromedriver')
driver.get("https://bit.ly/3kUS3do")
time.sleep(7)

req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')

thumbnails = soup.select("#imgList > div > a > img")

i = 1
for thumbnail in thumbnails:
    src = thumbnail["src"]
    dload.save(src,f'img_homework/{i}.jpg')
    i += 1

driver.quit()