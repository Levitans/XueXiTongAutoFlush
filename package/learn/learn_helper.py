# -*- encoding = utf-8 -*-
# @Time : 2022-04-16 0:08
# @Author : Levitan
# @File : learn_helper.py
# @Software : PyCharm
import random
import time
import traceback

from package.learn import globalvar as gl
from package.learn import exception as myException
from package.learn.driver.mydriver import MyDriver
from package.learn.school.getter import schoolGetter
from package.learn.task.quiz.quiz import QuizOfTask
from package.learn.task.audio import Audio
from package.learn.task.video import Video
from package.learn.task.ppt import PPT

from package.learn.data_management.datamanger import ExceptionLevel as errLevel

from package.learn.printer import color
from package.learn.printer.factory import getPrinterBySetter
from package.learn.printer.setter import TableSetter

import package.learn.driver

from selenium.webdriver.common.by import By
from selenium.common import exceptions

# 该方法获页面中的课程，并返回用户选择的课程
def getCourse(driver: MyDriver, learn):
    # 获取所有课程
    driver.go_courses_page()
    try:
        courses_list = learn.get_courses(driver.get_driver())
    except exceptions.NoSuchElementException as e:
        errInfo = traceback.format_exc()
        gl.exception_log_manger.writeLog(gl.version, errInfo)
        raise Exception("获取课程时出现异常：" + str(e) + "\n可能原因见：package\\learn\\school\\README.md")

    # 以表格的形式打印课程

    # 设置表格的外观
    mySetter = TableSetter()
    mySetter.hasHead = True
    mySetter.autoOrdNumber = True
    mySetter.headColor = "green"
    mySetter.abreastTableNumber = 2
    tablePrinter = getPrinterBySetter(mySetter)
    tablePrinter.setTableColWidth([30])

    # 设置需要打印的数据
    courseNameList = [["课程名"]]
    courseNameList += [[i.name] for i in courses_list]

    # 打印
    print(color.blue("当前课程有："))
    tablePrinter.print(courseNameList)

    # 读取用户指定的课程
    index = int(input("\n输入课程序号：")) - 1
    course = courses_list[index]
    gl.spliter.print()
    return course


def automatic_learning(driver: MyDriver, specificChapter=False):
    """
        learn = fuist
        这一句是指定学校
        不同的学校对应 package/learn/school 下的一个 .py 文件
        如果程序运行时没有找到课程，或者进入课程后没有找到章节，则大概率是因为学校不同导致页面元素不同。
        详细解决方案看 package/learn/school/README.md
    """
    learn = schoolGetter(gl.school_type)
    course = getCourse(driver, learn)
    # 获取所有章节
    try:
        driver.get_url(course.get_ZJ_path())
        driver.driver_wait(By.CLASS_NAME, "chapter_td")
    except myException.TimeoutException as e:
        raise Exception("章节页面未成功加载："+str(e))
    try:
        chapter_list = learn.get_chapters(driver.get_driver())
    except exceptions.NoSuchElementException as e:
        errInfo = traceback.format_exc()
        gl.exception_log_manger.writeLog(errInfo, errLevel.high)
        raise Exception("获取章节时出现异常："+str(e)+"\n可能原因见：package\\learn\\school\\README.md")

    # 跳过已完成的章节
    for i in chapter_list:
        if not gl.judgment_TP_tate:
            print(color.yellow("当前程序不自动跳过已完成章节"))
            print(color.yellow("若需要开启自动跳过已完成章节功能\n请前往 config.ini 文件修改"))
            i.webElement.click()
            break
        if i.isFinish:
            print("章节：" + color.green(i.toString()) + " 已经完成")
        else:
            print("章节：" + color.blue(i.toString()) + " 未完成")
            if not specificChapter:
                i.webElement.click()
                break

    if specificChapter:
        while True:
            starCatalogSbar = input(color.blue("输入章节号（例如：1.1）："))
            for i in chapter_list:
                if i.catalog_sbar == starCatalogSbar:
                    i.webElement.click()
                    break
            else:
                print(color.yellow("章节号不存在，请重新输入！！"))
                continue
            break
    gl.spliter.print()

    driver.driver_wait(By.CSS_SELECTOR, '[id="iframe"]')
    # 收起目录栏
    driver.getElement(By.CLASS_NAME, "switchbtn").click()
    time.sleep(1)
    driver.go_js("var q=document.documentElement.scrollTop=10000")
    time.sleep(0.5)

    # 循环所有章节
    while True:
        # 寻找是否有任务卡
        prev_table_list = []
        try:
            prev_table_list = driver.getElement(By.CSS_SELECTOR, '[class="prev_tab"]') \
                .find_element(By.CSS_SELECTOR, '[class="prev_ul"]') \
                .find_elements(By.TAG_NAME, 'li')
        except exceptions.NoSuchElementException:
            pass
        prev_table_number = len(prev_table_list) if len(prev_table_list) != 0 else 1  # 选项卡个数
        print("当前章节选项卡有 " + str(prev_table_number) + " 个")

        # 遍历每个任务卡
        for tableIndex in range(prev_table_number):
            # 第一个任务卡不用点击
            if tableIndex != 0:
                item = prev_table_list[tableIndex].find_element(By.TAG_NAME, 'div')
                driver.get_driver().execute_script("arguments[0].scrollIntoView(false);", item)
                item.click()
                time.sleep(1)

            # 进入第一层iframe
            driver.get_driver().switch_to.frame("iframe")

            # 获取任务点
            """
                iframeList 是一个列表，其中存的是任务点的 WebElement 对象
                taskPointFinishStateList 是一个列表，其中存的是每个任务点的状态
                
                    iframeList中的元素与taskPointFinishStateList中的元素一一对应
            """
            iframeList = driver.getElements(By.TAG_NAME, 'iframe')
            print("当前章节有 " + color.yellow(str(len(iframeList))) + " 个任务点")

            # 获取当前页面中任务点的状态
            """
                taskPointFinishStateList 中储存任务点状态
                任务点状态为以下三种之一
                    1、任务点未完成
                    2、任务点完成
                    3、任务点状态无法判断
            """
            taskPointFinishStateList = []
            for i in iframeList:
                taskPoint = i.find_element(By.XPATH, "../.")    # 获取任务点的爷爷元素
                taskPointClass = taskPoint.get_attribute("class")
                if taskPointClass is None:              # 任务点状态无法判断
                    taskPointFinishStateList.append(3)
                elif taskPointClass == "ans-attach-ct":
                    taskPointFinishStateList.append(1)  # 任务点未完成
                elif taskPointClass == "ans-attach-ct ans-job-finished":
                    taskPointFinishStateList.append(2)  # 任务点已完成
                else:
                    taskPointFinishStateList.append(3)  # 任务点状态无法判断

            # 遍历每个任务点
            for i in range(len(iframeList)):
                print("当前为第 " + color.blue(str(i + 1)) + " 任务点")

                # 判断任务点状态
                if gl.judgment_TP_tate and taskPointFinishStateList[i] == 3:
                    print(color.yellow("当前任务点无法判断其状态"))
                    print(color.yellow("跳过当前任务点")+"\n")
                    time.sleep(random.randint(3, 5))
                    continue
                elif gl.judgment_TP_tate and taskPointFinishStateList[i] == 2:
                    print(color.green("当前任务点已完成"))
                    print(color.green("跳过当前任务点")+"\n")
                    time.sleep(random.randint(3, 5))
                    continue
                elif gl.judgment_TP_tate and taskPointFinishStateList[i] == 1:
                    print(color.green("当前任务点未完成"))
                    print(color.green("开始学习当前任务点"))
                # 循环判断任务点类型
                # 因为当前 QuizOfTask 类型任务点还没有欧判读方法，所以 QuizOfTask 任务放在元组最后面
                for item in (PPT, Video, Audio, QuizOfTask):
                    task = item(driver.get_driver())
                    if task.isCurrentTask(i):
                        print("当前任务点是 " + color.green(task.__name__))
                        driver.get_driver().switch_to.frame(iframeList[i])
                        try:
                            task.finish()
                            break
                        except Exception as e:
                            errInfo = traceback.format_exc()
                            errInfo += "以 {} 执行时出错".format(task.__name__)
                            gl.exception_log_manger.writeLog(gl.version, errInfo, errLevel.middle)
                            driver.get_driver().switch_to.default_content()
                            gl.errorPrinter.print("当前任务点 {} 运行时出错\n详细错误信息已写入 exception.log 中".format(task.__name__))
                            print("跳过当前任务点")
                            break
                    else:
                        print("当前任务点不是 " + color.yellow(task.__name__))
                gl.spliter.print()
                driver.get_driver().switch_to.default_content()
                driver.get_driver().switch_to.frame("iframe")
                iframeList = driver.getElements(By.TAG_NAME, 'iframe')
            # 完成当前章节后退出到最外层
            # 不退出到最外层就无法找到”下一章节“的按钮
            driver.get_driver().switch_to.default_content()

        print("当前章节已完成")
        print(color.green("完成时间："+getTimeStr()))
        gl.spliter.print()

        # 判断有没有出现章节提示
        chapterTips = driver.is_element_presence(By.CSS_SELECTOR, '[class="popDiv wid440 popMove"]')
        if chapterTips is not None:
            chapterTips.find_element(By.CLASS_NAME, '[class="jb_btn jb_btn_92 fr fs14 nextChapter"]').click()

        next_button = driver.is_element_presence(By.CSS_SELECTOR, '[class="jb_btn jb_btn_92 fs14 prev_next next"]')
        if next_button is not None:
            next_button.click()
            driver.driver_wait(By.CLASS_NAME, "course_main")
        else:
            print("课程学习完毕")
            exit()


def do_homework(driver: MyDriver):
    # 做作业的功能等待实现
    pass


def getTimeStr():
    timeFormat = "%Y年%m月%d日 %H时%M分%S秒"
    return time.strftime(timeFormat, time.localtime())



