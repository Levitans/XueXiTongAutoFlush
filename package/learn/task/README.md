# task 目录说明

---

### 一
该目录存放当前程序能完成的**任务类型**，分别是：测验（quiz目录）、音频（audio.py）、视频（video.py）、PPT（ppt.py）
其中实现 **quiz** 功能的代码较多所以单独放在一个目录中

### 二
每个任务类型都抽象为一个 class ，并且每个任务类型类都继承 **interface.py** 中的的 Task 接口。
Task 接口提供 **isCurrentTask()** 和 **finish()** 两个方法。

**isCurrentTask()：** 判断任务点是否为该任务类型。  
**finish()：** 完成当前任务点。