from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import json
import csv

from builtins import set
from idlelib.iomenu import encoding
from test.sortperf import flush
# import codecs
#read course urls from json file
with open('course.json','r') as fp:
    cUrls = json.load(fp)
print("Read Course Urls Finished!")
fp.close()
# f = open('courseInformation_test.txt', encoding = 'utf-8')
# for line2 in open('courseInformation_test.txt', encoding = 'utf-8'):
#     print(line2)
driver = webdriver.Chrome()

#course information list
# courses_list = []
# old_cUrls = []
#error course urls
errorUrls = []
with open('courseInformation.txt','a', encoding = 'utf-8') as fp:
#     fp.write(codecs.BOM_UTF8)
#     writer.writerow(['课程名称', '开设高校', '所属类别', '教师', '开课次数', '学期信息', '课程简介', '课程概述等', '课程评价数', '课程平均评分', '学生评价', '课程链接'])
    for cUrl in cUrls:
#         print(cUrl)
        driver.get(cUrl)
        time.sleep(2)
        #课程名称
        name = driver.find_element_by_class_name('course-title.f-ib.f-vam').text
#         print('课程名称:', name, file = fp)
#         print(name)
        #所属类别
        try:
            category = driver.find_element_by_class_name('breadcrumb_item.sub-category').text
        except NoSuchElementException:
            category = 'None'
#         print(category)
#         print('所属类别:', category, file = fp)
        #学期开课信息
        term_info = []
        #开课时间
        term_time = driver.find_element_by_class_name('course-enroll-info_course-info_term-info_term-time').text
    #     print(term_time)
        #学时安排
        term_workload = driver.find_element_by_class_name('course-enroll-info_course-info_term-workload').text
    #     print(term_workload)
        term_info.append({term_time, term_workload})
        #开课次数
        term_number = 1
        
        #当前学期
        term_selected = 2
        
        #选择不同的学期，获取开课信息
        try:
            while True:
                term_select = driver.find_element_by_class_name('ux-dropdown.course-enroll-info_course-info_term-select_dropdown')
                term_select.click()
                term = driver.find_elements_by_class_name('f-thide.th-fs0fc5')
                #开课次数  更新
                term_number = len(term)
                next_term = term_number - term_selected
                try:
                    term[next_term].click()
                except ElementNotInteractableException:
                    errorUrls.append(cUrl)
                    break
                time.sleep(2)
                #开课时间
                term_time = driver.find_element_by_class_name('course-enroll-info_course-info_term-info_term-time').text
    #             print(term_time)
                #学时安排
                term_workload = driver.find_element_by_class_name('course-enroll-info_course-info_term-workload').text
    #             print(term_workload)
                term_info.append({term_time, term_workload}) 
                term_selected = term_selected + 1
                if next_term == 0:
                    break
        except NoSuchElementException:
            term_number = 1
#         print('term number:',term_number)
#         print(term_info)
        #课程所属学校名称
        university = driver.find_element_by_class_name('u-img').get_attribute('alt')
#         print('开设高校:', university, file = fp)
#         print(university)
        #授课教师信息：姓名 职称 多页
        teachers_list = []
        while True:
            teachers = driver.find_elements_by_class_name('cnt.f-fl')
            for tea in teachers:
                teacher_info = tea.text
                teachers_list.append(teacher_info.split())
            try:
                slider_next = driver.find_element_by_class_name('u-icon-arrow-right-thin.f-ib.f-pa')
                driver.execute_script("arguments[0].click();", slider_next)
            except NoSuchElementException:
                break
#         print('教师:', teachers_list, file = fp)
#         print(teachers_list)
        #简介-课程团队
        try:
            course_intro = driver.find_element_by_class_name('course-heading-intro_intro').text
        except NoSuchElementException:
            course_intro = 'None'
            
#         print(course_intro)
        #课程概述、授课目标、课程大纲、参考资料、证书要求
        course_overview = driver.find_elements_by_class_name('category-content.j-cover-overflow')
        course_overview_text = []
        for c in course_overview:
            course_overview_text.append(c.text)
        
#         print(course_overview_text)
        #课程评价
        review_button = driver.find_element_by_id('review-tag-button')
        review_button.click()
        #评价数
        review_num = driver.find_element_by_id('review-tag-num').text
        review_num = review_num.replace('(','').replace(')','')
#         print(review_num)
        #课程评分
        try:
            review_score = driver.find_element_by_class_name('ux-mooc-comment-course-comment_head_rating-scores').text
        except NoSuchElementException:
            review_score = 'None'
#         print(review_score)
        #学员评价
        course_comments = []
        while True:
            try:
                comments = driver.find_elements_by_class_name('ux-mooc-comment-course-comment_comment-list_item')
            except NoSuchElementException:
                break
            for comment in comments:
                #学员姓名
                #stale element reference: element is not attached to the page document
                staleElement = True
                while staleElement:
                    try:
                        user_name = comment.find_element_by_class_name('primary-link.ux-mooc-comment-course-comment_comment-list_item_body_user-info_name').text
                        #学员评分
                        star = len(comment.find_element_by_class_name('star-point').find_elements_by_tag_name('i'))
                        #学员评语 更多
                        try:
                            comment_more = comment.find_element_by_class_name('ux-mooc-comment-course-comment_comment-list_item_body_content_more-btn primary-link-underline')
                            driver.execute_script("arguments[0].click();", comment_more)
                            comment_text = comment.find_element_by_class_name('ux-mooc-comment-course-comment_comment-list_item_body_content').text
                        except NoSuchElementException:
                            comment_text = comment.find_element_by_class_name('ux-mooc-comment-course-comment_comment-list_item_body_content').text
#                         print(comment_text)        
                        #发表日期
                        comment_date = comment.find_element_by_class_name('ux-mooc-comment-course-comment_comment-list_item_body_comment-info_time').text
                        #所在学期
                        term_signed = comment.find_element_by_class_name('ux-mooc-comment-course-comment_comment-list_item_body_comment-info_term-sign').text
                        #评论点赞数
                        comment_vote = comment.find_element_by_class_name('ux-mooc-comment-course-comment_comment-list_item_body_comment-info_actions_vote').text
                        staleElement = False
                    except StaleElementReferenceException:
                        staleElement = True
                course_comments.append({'user_name':user_name,'star':star,'content':comment_text,'date':comment_date,'term':term_signed,'vote':comment_vote})
            #翻页
            try:
                page = driver.find_element_by_class_name('ux-pager_btn.ux-pager_btn__next')
                #ElementClickInterceptedException: Message: element click intercepted
                driver.execute_script("arguments[0].click();", page)
                time.sleep(3)
            except NoSuchElementException:
                break
            try:
                page.find_element_by_class_name('th-bk-disable-gh')
                break
            except NoSuchElementException:
                continue
#         print(course_comments)
    #     course = {'course name':name, 'university': university, 'category':category, 'teachers': teachers_list, 'term number':term_number, 'term_info':term_info, 'course introduction':course_intro, 'course overview':course_overview_text, 'review number': review_num, 'overall score':review_score, 'comments':course_comments, 'url':cUrl} 
#         course = [name, university, category, teachers_list, term_number, term_info, course_intro, course_overview_text, review_num, review_score, course_comments, cUrl] 
        print('课程名称:', name, file = fp)
        print('开设高校:', university, file = fp)
        print('所属类别:', category, file = fp)
        print('教师:', teachers_list, file = fp)
        print('开课次数:', term_number, file = fp)
        print('学期信息:', term_info, file = fp)
        print('课程简介:', course_intro, file = fp)
        print('课程概述等:', course_overview_text, file = fp)
        print('课程评价数:', review_num, file = fp)
        print('课程平均评分:', review_score, file = fp)
        print('学生评价:', course_comments, file = fp)
        print('课程链接:', cUrl, file = fp)
        fp.flush()
#         print(course, file = fp)
#         fp.write(course)
#         json.dump(course, fp = fp, skipkeys = True, ensure_ascii = False, indent = 4)
#     old_cUrls.append(cUrl)
    
# with open('oldcUrls.json','w') as fp:
#     json.dump(old_cUrls, fp = fp, skipkeys = True, ensure_ascii = False, indent = 4)
fp.close()
with open('errorCourseUrls_test.json','w') as fp:
    json.dump(errorUrls, fp = fp, skipkeys = True, ensure_ascii = False, indent = 4)
fp.close()
driver.close()

# with open('courseInformation.json','w') as fp:
#     json.dump(courses_list, fp = fp, skipkeys = True, ensure_ascii = False, indent = 4)
