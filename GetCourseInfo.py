from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
        
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import json
from builtins import set
with open('course.json','r') as fp:
    cUrls = json.load(fp)
print("Read Course Urls Finished!")

driver = webdriver.Chrome()
courses_list = []
old_cUrls = []
errorUrls = []
for cUrl in cUrls:
    print('Course Url:',cUrl)
    driver.get(cUrl)
    time.sleep(2)
    #课程名称
    name = driver.find_element_by_class_name('course-title.f-ib.f-vam').text
#     print(name)
    #所属类别
    category = driver.find_element_by_class_name('breadcrumb_item.sub-category').text
#     print(category)
   
    #开课时间
    term_info = []

    
    term_time = driver.find_element_by_class_name('course-enroll-info_course-info_term-info_term-time').text
#     print(term_time)
    term_workload = driver.find_element_by_class_name('course-enroll-info_course-info_term-workload').text
#     print(term_workload)
    term_info.append({term_time, term_workload})
     #开课次数
    term_number = 1
    
    #当前学期
    term_selected = 2
    
    try:
        while True:
            term_select = driver.find_element_by_class_name('ux-dropdown.course-enroll-info_course-info_term-select_dropdown')
            term_select.click()
            term = driver.find_elements_by_class_name('f-thide.th-fs0fc5')
            term_number = len(term)
            next_term = term_number - term_selected
            try:
                term[next_term].click()
            except ElementNotInteractableException:
                errorUrls.append(cUrl)
                break
            time.sleep(2)
            term_time = driver.find_element_by_class_name('course-enroll-info_course-info_term-info_term-time').text
#             print(term_time)
            term_workload = driver.find_element_by_class_name('course-enroll-info_course-info_term-workload').text
#             print(term_workload)
            term_info.append({term_time, term_workload}) 
            term_selected = term_selected + 1
            if next_term == 0:
                break
    except NoSuchElementException:
        term_number = 1
    print('term number:',term_number)
    #学校名称
    university = driver.find_element_by_class_name('u-img').get_attribute('alt')
    
    #授课教师信息：姓名 职称
    teachers_list = []
    teachers = driver.find_elements_by_class_name('cnt.f-fl')
    for tea in teachers:
        teacher_info = tea.text
        teachers_list.append(teacher_info.split())

    #课程团队建议
    course_intro = driver.find_element_by_class_name('course-heading-intro_intro').text
#     print(course_intro)
#     #课程概述
#     course_overview = driver.find_element_by_class_name('f-richEditorText').find_elements_by_tag_name('span')
#     course_overview_text = ''
#     for paragraph in course_overview:
#         course_overview_text = course_overview_text + paragraph.text
# #     print(course_overview_text)
#     #课程大纲
#     course_outline = driver.find_element_by_class_name('outline').text
    #课程概述、授课目标、课程大纲、参考资料、证书要求
    course_overview = driver.find_elements_by_class_name('category-content.j-cover-overflow')
    course_overview_text = []
    for c in course_overview:
        course_overview_text.append(c.text)
    #课程评价
    review_button = driver.find_element_by_id('review-tag-button')
    review_button.click()
    #评价数
    review_num = driver.find_element_by_id('review-tag-num').text
    review_num = review_num.replace('(','').replace(')','')
#     print(review_num)
    #课程评分
    try:
        review_score = driver.find_element_by_class_name('ux-mooc-comment-course-comment_head_rating-scores').text
    except NoSuchElementException:
        review_score = 'None'
    print(review_score)
    #学员评价
    course_comments = []
    while True:
        comments = driver.find_elements_by_class_name('ux-mooc-comment-course-comment_comment-list_item')
        for comment in comments:
            #学员姓名
            user_name = comment.find_element_by_class_name('primary-link.ux-mooc-comment-course-comment_comment-list_item_body_user-info_name').text
            #学员评分
            star = len(comment.find_element_by_class_name('star-point').find_elements_by_tag_name('i'))
            #学员评语
            comment_text = comment.find_element_by_class_name('ux-mooc-comment-course-comment_comment-list_item_body_content').text
            #发表日期
            comment_date = comment.find_element_by_class_name('ux-mooc-comment-course-comment_comment-list_item_body_comment-info_time').text
            #所在学期
            term_signed = comment.find_element_by_class_name('ux-mooc-comment-course-comment_comment-list_item_body_comment-info_term-sign').text
            #评论点赞数
            comment_vote = comment.find_element_by_class_name('ux-mooc-comment-course-comment_comment-list_item_body_comment-info_actions_vote').text
            course_comments.append({'user_name':user_name,'star':star,'content':comment_text,'date':comment_date,'term':term_signed,'vote':comment_vote})
        #翻页
        try:
            page = driver.find_element_by_class_name('ux-pager_btn.ux-pager_btn__next')
            page.click()
            time.sleep(2)
        except NoSuchElementException:
            break
        try:
            page.find_element_by_class_name('th-bk-disable-gh')
            break
        except NoSuchElementException:
            continue
    
    courses_list.append({'course name':name, 'university': university, 'category':category, 'teachers': teachers_list, 'term number':term_number, 'term_info':term_info, 'course introduction':course_intro, 'course overview':course_overview_text, 'review number': review_num, 'overall score':review_score, 'comments':course_comments, 'url':cUrl}) 
    old_cUrls.append(cUrl)
    
with open('oldcUrls.json','w') as fp:
    json.dump(old_cUrls, fp = fp, skipkeys = True, ensure_ascii = False, indent = 4)
    
with open('errorCourseUrls.json','w') as fp:
    json.dump(errorUrls, fp = fp, skipkeys = True, ensure_ascii = False, indent = 4)

with open('courseInformation.json','w') as fp:
    json.dump(courses_list, fp = fp, skipkeys = True, ensure_ascii = False, indent = 4)

     
        
    