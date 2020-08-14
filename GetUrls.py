# from selenium import webdriver
# import time
# driver = webdriver.Chrome()
# url = "https://www.icourse163.org/university/view/all.htm#/"
# driver.get(url)
# driver.implicitly_wait(10)
# universityURL = driver.find_elements_by_class_name('u-usity f-fl')# list of all universitie URL
# for ele in universityURL:
#     content = ele.find_element_by_xpath("//*[@id=\"g-body\"]/div/div[2]/div[2]/a[1]/img")
###################################
# import requests
# import chardet
# from bs4 import BeautifulSoup
# from collections import namedtuple
# r = requests.get('https://www.icourse163.org/university/PKU')
# r.encoding = chardet.detect(r.content)['encoding']
# # r.encoding = 'utf-8'
# print(r.text)
from lxml.html.diff import href_token
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from _csv import Dialect

# import re
# URLPattern = re.compile(r'<a class=\"u-usity f-fl\".*>')
# URLResult = re.findall(URLPattern, r.text) #list
#print(URLResult)

# NamePattern = re.compile(r'alt=.*"')
# NameResult = re.findall(NamePattern, r.text)
#print(NameResult)
###################################
'''import json
soup = BeautifulSoup(r.text, 'lxml')
URLNameReuslt = soup.find_all("a", class_="u-usity f-fl")
URLUniList = []
for a in URLNameReuslt:
    href = a.get('href')
#     print(href)
    i = a.find('img')
    name = i.get('alt')
#     URLUniList.append({'href': href,'University': name}) # for json
    content = (href,name) # for csv
    URLUniList.append(content) # for csv'''
#     print(name)
# with open('unilist.json','w') as fp:
#     json.dump(URLUniList, fp = fp, skipkeys = True, ensure_ascii = False, indent = 4)
# 
# with open('unilist.json','r') as fp:
#     print(json.load(fp))
# 
# import csv
# 
# headers = ['href','University']
# with open('unilist.csv','w') as f:
#     f_csv = csv.writer(f)
#     f_csv.writerow(headers)
#     f_csv.writerows(URLUniList)
############################################
# with open('unilist.csv') as f:
#     f_csv = csv.DictReader(f)
#     for row in f_csv:
#         print(row.get('href'), row.get('University'))
        
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from urllib.parse import urljoin
driver = webdriver.Chrome()
driver.get("https://www.icourse163.org/university/view/all.htm#/")
#time.sleep(5)
university = driver.find_elements_by_class_name('u-usity.f-fl')
uniUrls = []
cUrls = []
errorUrl = []

for uni in university:
    uniUrl = uni.get_attribute('href')
    uniUrls.append(uniUrl)

print("Obtain Course Finished!")

import json
with open('university.json','w') as fp:
    json.dump(uniUrls, fp = fp, skipkeys = True, ensure_ascii = False, indent = 4)
    
print("Write University Finished!")

for uniUrl in uniUrls:
    driver.get(uniUrl) # enter the page of the course list 
    time.sleep(2)
    while True: # obtain all the course urls
        #if arrive the last page
        try:
            course = driver.find_element_by_class_name('u-courseCardWithTime-container_a160')
        except NoSuchElementException:
            errorUrl.append(uniUrl)
            break
        cUrl = course.get_attribute('href')
        if cUrls.__contains__(cUrl):
                break
        
        course = driver.find_elements_by_class_name('u-courseCardWithTime-container_a160')
        for c in course:
            cUrl = c.get_attribute('href')
            cUrls.append(cUrl)
        
        try:
            page = driver.find_element_by_class_name('zbtn.znxt') #the first next button
            page.click()
            time.sleep(2)
        except NoSuchElementException:
            errorUrl.append(uniUrl)
            continue

print("Obtain Course Finished!")

with open('course.json','w') as fp:
    json.dump(cUrls, fp = fp, skipkeys = True, ensure_ascii = False, indent = 4)

print("Write Course Finished!")

with open('errorurl.json','w') as fp:
    json.dump(errorUrl, fp = fp, skipkeys = True, ensure_ascii = False, indent = 4)

print("Write Error Url Finished!")
