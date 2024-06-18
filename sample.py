# 引入模組
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 初始化 WebDriver
def initialize_driver():
    driver = webdriver.Chrome()
    driver.get("https://sss.must.edu.tw/RWD_CosInfo/")
    return driver

# 搜尋課程
def search_course(driver, course_name):
    search = driver.find_element(By.NAME, "cosn")
    search.send_keys(course_name)
    search.send_keys(Keys.RETURN)
    time.sleep(4)

# 爬取課程資訊
def scrape_courses(driver, max_pages=2):
    courses = []
    page_count = 0

    while page_count < max_pages:
        try:
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "dynamic-table"))
            )
        except:
            break

        rows = table.find_elements(By.TAG_NAME, "tr")

        for row in rows[1:]:
            cols = row.find_elements(By.TAG_NAME, "td")
            course_info = {
                "部別": cols[0].text,
                "課名": cols[2].text,
                "開課班級": cols[4].text,
                "學分": cols[5].text,
                "時數": cols[6].text,
                "選別": cols[7].text,
                "人數限制": cols[8].text,
                "修課人數": cols[9].text,
                "授課教師": cols[10].text,
                "教室": cols[11].text,
                "上課時間": cols[12].text,
                "課程大綱": cols[13].text,
                "跨系選課": cols[14].text
            }
            courses.append(course_info)

        try:
            next_button = driver.find_element(By.LINK_TEXT, "下一頁")
            if "disabled" in next_button.get_attribute("class"):
                break
            next_button.click()
            time.sleep(4)
            page_count += 1
        except:
            break
    return courses

# 輸出課程資訊
def print_course(course):
    print("部別: {}\n課名: {}\n開課班級: {}\n學分: {}\n時數: {}\n選別: {}\n人數限制: {}\n修課人數: {}\n授課教師: {}\n教室: {}\n上課時間: {}\n課程大綱: {}\n跨系選課: {}\n".format(
        course["部別"],
        course["課名"],
        course["開課班級"],
        course["學分"],
        course["時數"],
        course["選別"],
        course["人數限制"],
        course["修課人數"],
        course["授課教師"],
        course["教室"],
        course["上課時間"],
        course["課程大綱"],
        course["跨系選課"]
    ))
    print("-" * 20)

# 選擇課程
def select_course(courses):
    selected_courses = []

    print("\n")
    selected_course_number = input("請輸入您要選擇的課程的班級：").upper()

    filtered_courses = [course for course in courses if course["開課班級"] == selected_course_number]

    if not filtered_courses:
        print("找不到開課班級為 {} 的課程。".format(selected_course_number))
    else:
        selected_courses.append(filtered_courses[0])
        print("已選擇以下課程：")
        for course in filtered_courses:
            print_course(course)

    return selected_courses

# 檢查時間衝突
def check_time_conflicts(selected_courses):
    time_slots = {}
    conflicts = False

    for course in selected_courses:
        class_times = course["上課時間"].split(", ")
        for time_slot in class_times:
            if time_slot in time_slots:
                print("衝堂：{} 與 {} 課程在 {} 時有衝突".format(course["開課班級"], time_slots[time_slot]["開課班級"], time_slot))
                conflicts = True
            else:
                time_slots[time_slot] = course

    if conflicts:
        drop_course_number = input("請輸入要放棄的課程的開課班級：").upper()
        selected_courses = [course for course in selected_courses if course["開課班級"] != drop_course_number]
        print("\n已放棄開課班級為 {} 的課程。".format(drop_course_number))
        print("\n您已選擇以下課程：")
        for course in selected_courses:
            print_course(course)
    else:
        print("您選擇的課程沒有衝堂。")

    return selected_courses

# 從一開始執行到選擇課程的步驟
driver = initialize_driver()
search_course(driver, "電子學")
courses = scrape_courses(driver)
for course in courses:
    print_course(course)

selected_courses = select_course(courses)
print("\n您已選擇以下課程：")
for course in selected_courses:
    print_course(course)
