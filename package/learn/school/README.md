# school 目录说明

---

### 文件说明：
该文件夹中除了 **template.py** 文件。其余 **\*.py** 都代表一个学校，格式为 **学校名.py**

### 问题：
因为学校不同，学习通的页面中元素的属性可能不同。

例如，有的学校在课程标签的属性中有 class="color1" 所以程序可以通过 class="color1" 来定位课程标签。而别的学校课程标签中 class 的值不一定为 
"color1" 程序运行就会出现异常。  
会出现部分人使用程序可以获取课程，部分人无法获取课程

### 解决方式：
目前这个问题还没有很好的解决方法。  
当前的解决方法是，如果有遇到这个问题就自己写一个适合自己学校的函数。  
**按照以下约定**来写函数可以很方便的和程序兼容

#### 约定
在 **school** 文件中，新建一个python文件，文件命名就看个人喜好或者自己学校的简称能区分不同学校即可，在新建的python文件中实现下面两个函数

**def get_courses(driver) -> list[Course]**  
**主要功能：** 获取页面的所有课程。  
**参数：driver** 一个 WebDriver 实例  
**范围值：** 一个列表，列表中为 Course 的实例（Course 详见 package\learn\school\template.py）  


**def get_chapters(driver) -> list[Chapter]**
**主要功能：** 获取页面的所有章节 
**参数：driver** 一个 WebDriver 实例  
**范围值：** 一个列表，列表中为 Chapter 的实例（Chapter 详见 package\learn\school\template.py）  

