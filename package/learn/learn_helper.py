# -*- encoding = utf-8 -*-
# @Time : 2022-04-16 0:08
# @Author : Levitan
# @File : learn_helper.py
# @Software : PyCharm
import time

from package.learn import globalvar as gl
from package.learn import color
from package.learn.mydriver import MyDriver
from package.learn.school import fuist
from package.learn.display import Display, MyFormat
from package.learn.task.quiz.quiz import Quiz
from package.learn.task.audio import Audio
from package.learn.task.video import Video
from package.learn.task.ppt import PPT

from selenium.webdriver.common.by import By
from selenium.common import exceptions

def automatic_learning(driver):
    learn = fuist
    driver.go_courses_page()

    # 获取所有课程
    courses_list = learn.get_courses(driver.get_driver())
    print(color.blue("当前课程有："))
    Display.printTable([i.name for i in courses_list], MyFormat([50, 50], displayNumber=True))
    index = int(input("\n输入课程序号：")) - 1
    course = courses_list[index]
    Display.separate()

    # 获取所有章节
    driver.get_url(course.get_ZJ_path())
    driver.driver_wait(By.CLASS_NAME, "chapter_td")
    chapter_list = learn.get_chapters(driver.get_driver())

    # 跳过已完成的章节
    for i in chapter_list:
        if i.isFinish:
            print("章节："+color.green(i.name)+" 已经完成")
        else:
            print("章节："+color.blue(i.name)+" 未完成")
            i.webElement.click()
            break
    Display.separate()

    # 收起目录栏
    driver.get_driver().find_element(By.CLASS_NAME, "switchbtn").click()
    time.sleep(1)
    driver.go_js("var q=document.documentElement.scrollTop=10000")
    time.sleep(0.5)

    # 循环所有章节
    while True:
        # 寻找是否有选项卡
        prev_table_list = []
        try:
            prev_table_list = driver.get_driver().find_element(By.CSS_SELECTOR, '[class="prev_tab"]') \
                         .find_element(By.CSS_SELECTOR, '[class="prev_ul"]') \
                         .find_elements(By.TAG_NAME, 'li')
        except exceptions.NoSuchElementException:
            pass
        prev_table_number = len(prev_table_list) if len(prev_table_list) !=0 else 1  # 选项卡个数
        print("当前章节选项卡有 "+str(prev_table_number)+" 个")

        # 遍历每个选项卡
        for tableIndex in range(prev_table_number):
            # 第一个选项卡不用点击
            if tableIndex != 0:
                item = prev_table_list[tableIndex].find_element(By.TAG_NAME, 'div')
                driver.get_driver().execute_script("arguments[0].scrollIntoView(false);", item)
                item.click()
                time.sleep(1)

            # 进入第一层iframe
            driver.get_driver().switch_to.frame("iframe")
            iframeList = driver.get_driver().find_elements(By.TAG_NAME, 'iframe')
            print("当前章节有 "+color.yellow(str(len(iframeList)))+" 个任务点")

            # 遍历每个任务点
            for i in range(len(iframeList)):
                print("当前为第 "+color.blue(str(i+1))+" 任务点")

                # 循环判断任务点类型
                # 因为当前 Quiz 类型任务点还没有欧判读方法，所以 Quiz 任务放在元组最后面
                for item in (PPT, Video, Audio, Quiz):
                    task = item(driver.get_driver())
                    if task.isCurrentTask(i):
                        print("当前任务点是 "+color.green(task.__name__))
                        driver.get_driver().switch_to.frame(iframeList[i])
                        try:
                            task.finish()
                            break
                        except Exception as e:
                            driver.get_driver().switch_to.default_content()
                            print(color.read("当前任务点 {} 运行时出错".format(task.__name__)))
                            print(color.read(str(e)))
                            print("跳过当前任务点")
                    else:
                        print("当前任务点不是 "+color.yellow(task.__name__))
                Display.separate()
                driver.get_driver().switch_to.default_content()
                driver.get_driver().switch_to.frame("iframe")
                iframeList = driver.get_driver().find_elements(By.TAG_NAME, 'iframe')
            driver.get_driver().switch_to.default_content()
        print("当前章节已完成")
        Display.separate()
        next_button = driver.is_element_presence(By.CSS_SELECTOR, '[class="jb_btn jb_btn_92 fs14 prev_next next"]')
        if next_button is not None:
            next_button.click()
            driver.driver_wait(By.CLASS_NAME, "course_main")
        else:
            print("课程学习完毕")
            exit()

def do_homework():
    pass

"""

https://mooc1.chaoxing.com/mooc2/work/list?
courseId=222737476
&
classId=50876312
&
cpi=156905667
&
ut=s&
enc=7d6f1269176623f37940cf4fab227ad1

https://mooc1-1.chaoxing.com/visit/stucoursemiddle?
courseid=222737476
&
clazzid=50876312
&
vc=1
&
cpi=156905667
&
ismooc2=1

"""