from selenium.common.exceptions import NoSuchElementException      
from selenium import webdriver
import time
driver = webdriver.Chrome()
#university page
driver.get("https://www.icourse163.org/university/view/all.htm#/")
university = driver.find_elements_by_class_name('u-usity.f-fl')

#university urls
uniUrls = []
#course urls
cUrls = []
#error urls
errorUrl = []

#get university urls
for uni in university:
    uniUrl = uni.get_attribute('href')
    uniUrls.append(uniUrl)

print("Obtain University Finished!")

#write university urls into json file
import json
with open('university.json','w') as fp:
    json.dump(uniUrls, fp = fp, skipkeys = True, ensure_ascii = False, indent = 4)
    
print("Write University Finished!")

#get course urls
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

#write course urls into json file
with open('course.json','w') as fp:
    json.dump(cUrls, fp = fp, skipkeys = True, ensure_ascii = False, indent = 4)

print("Write Course Finished!")

#write error urls into json file
with open('errorurl.json','w') as fp:
    json.dump(errorUrl, fp = fp, skipkeys = True, ensure_ascii = False, indent = 4)

print("Write Error Url Finished!")
