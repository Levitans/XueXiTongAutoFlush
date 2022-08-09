# printer 包介绍

---

> printer 包的作用是提供格式化的打印数据的功能，如打印表格、消息和分隔线等。  
> 该包使用了模板方法模式和工厂方法模式

## 1、模块介绍

printer 主要由3个模块, 分别是

- **打印器模块（printer.py）**

  > 打印模块中主存放打印器，**每个打印器都对应一个设置器**

  printer.py 中定义了打印器的模板（抽象父类）AbstractPrinter。AbstractPrinter规定每个打印器都必须*设置器（Setter类实例）*属性。

  目前printer.py中实现了3个打印器，分别是：

  - **表格打印器（TablePrinter）**

    *TablePrinter* 主要实现的是将结构化的数据在控制台中以表格的形式打印，可以自动计算表格列宽，也可以手动传入表格列宽并将超过宽度的数据进行缩略显示。

    还可以通过修改 *TableSetter* 的属性来自定义多种多样的表格外观。

    

  - **消息打印器（MsgPrinter）**

    *MsgPrinter* 主要功能是格式化的打印提示信息。

    可通过修改 *MsgSetter* 的属性来自定义打印消息的外观

    

  - **分隔线打印器（SplitPrinter）**

    *SplitPrinter* 主要功能是打印分隔线。

    可通过修改 *SplitSetter* 的属性来更改分隔线的外观和在分隔线中加入提示信息

    

- **设置器模块（setter.py）** 

  > 每一个设置器都对应一个打印器，设置器用户调整打印器打印的效果

  setter.py 模块中定义了所有打印器的设置器，其中的 AbstractSetter 是所有设置器的抽象父类

  - **表格设置器（TableSetter）**

    用于设置 *TablePrinter* 打印出的表格效果，如数据对齐方式、表头和表身颜色、是否自动计算宽度等。

    

  - **消息设置器（MsgSetter）**

    用于设置 *MsgPrinter* 打印出的消息效果

    

  - **分隔线设置器（SplitSetter）**

    用于设置 *SplitPrinter* 打印出的分隔线的效果

    

- **工厂模块（factory.py）**

  > 该模块中定义了获取各种 *打印器* 的方法

  - **getPrinterBySetter(setter: AbstractSetter) -> AbstractPrinter**

    该方法通过传入的设置器类型来实例化出对应的打印器实例，并将该打印器的 *_setter* 属性设置为传入的设置器

    

  - **getPrinterByName(printerName: str) -> AbstractPrinter**

    该方法通过传入的 *打印器类名* 来实例化对应的打印器。改方法实例化的打印器会使用默认的设置器。

    



## 2、使用演示



### TablePrinter

**示例代码**

~~~python
data = [["学号", "姓名",     "年级", "专业", "性别"],
        ["1001", "Levitan", "大三", "数据科学与大数据技术", "男"],
        ["1002", "Bob",     "大一", "数据科学与大数据技术"],
        ["1003", "Jack", "大二", "工程造价"],
        ["1004", "小红", "大四", "环境设计", "女"],
        ["1005", "小明", "大一", "", "男"]]

# 实例化配置类，修改配置信息
myCfg = TableSetter("demo")
myCfg.autoOrdNumber = True
myCfg.hasHead = True
myCfg.headColor = "blue"

a = getPrinterBySetter(myCfg)	# 获取显示器
a.print(data)	# 传入数据进行显示
~~~

**效果**

~~~
+------+-----------+---------+-----------+----------------------+--------+
| 序号 | StudentID | Name    | Grade     | Major                | Sex    |
+------+-----------+---------+-----------+----------------------+--------+
| 1    | 1001      | Levitan | junior    | Data Science         | male   |
+------+-----------+---------+-----------+----------------------+--------+
| 2    | 1002      | Bob     | freshmen  | Accounting           |        |
+------+-----------+---------+-----------+----------------------+--------+
| 3    | 1003      | Jack    | sophomore | Project Costs        |        |
+------+-----------+---------+-----------+----------------------+--------+
| 4    | 1004      | Alice   | senior    | Environmental Design | female |
+------+-----------+---------+-----------+----------------------+--------+
| 5    | 1005      | Tom     | freshmen  |                      | male   |
+------+-----------+---------+-----------+----------------------+--------+
~~~



### MsgPrinter

**示例代码**

~~~python
data = "Error in current program\n" \
       "Error reason: subscript out of bounds\n" \
       "You can view \"\\errorDemo\\README.md\" to solve this problem"
mySetter = MsgSetter()
mySetter.color = "read"
printer = getPrinterBySetter(mySetter)
printer.setSetter(mySetter)
printer.print(data)
~~~

**效果**

~~~
=============================================================
| Error in current program                                  |
| Error reason: subscript out of bounds                     |
| You can view "\errorDemo\README.md" to solve this problem |
=============================================================
~~~



### SplitPrinter

**示例代码**

~~~python
mySetter = SplitSetter()
mySetter.symbol = "="
mySetter.color = "green"
mySetter.length = 40
mySetter.message = ":I am the dividing line:"
mySetter.leftmostSymbol = "<"
mySetter.rightmostSymbol = ">"
printer = getPrinterBySetter(mySetter)
printer.print()
~~~

**效果**

~~~
<====================:I am the dividing line:====================>
~~~

