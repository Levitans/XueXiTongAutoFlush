# 当前目录下各文件的作用

## config.ini
程序配置文件，保存程序运行时的一些配置信息

**user_config**  
用户数据有关配置

|     选项名      |      作用       |  其他   |
|:------------:|:-------------:|:-----:|
|  user_path   |   账号密码文件路径    ||
| cookie_path  | cookie数据保存路径  ||

**browser_config**

|      选项名      |     作用     |      其他      |
|:-------------:|:----------:|:------------:|
|    no_head    | 是否开启浏览器显示  | False 或 True |
|    no_img     |  是否开启无图模式  | False 或 True |
|  mute_audion  |    是否静音    | False 或 True |
| browser_path  |   浏览器路径    ||
|  driver_path  |  浏览器驱动路径   ||


**task_config**  
答题功能配置

|            选项名             |      作用      |        其他        |
|:--------------------------:|:------------:|:----------------:|
|    decode_secret_status    |   字体解密器状态    |  0：关闭、1：开启、2：自动  |
|       ppt_speed_max        | ppt点击最长等待时间  |  不宜过快，不然会被学习通警告  |
|       ppt_speed_min        | ppt点击最短等待时间  |        同上        |
| quiz_get_answer_speed_max  |  答案获取最长等待时间  | 不宜过快，不然会被接口判定为爬虫 |
| quiz_get_answer_speed_min  |  答案获取最短等待时间  |        同上        |
|    quiz_click_speed_max    |  点击答案最长等待时间  |  不宜过快，不然会被学习通警告  |
|    quiz_click_speed_min    |  点击答案最短等待时间  |        同上        |


**other**
其他配置

|           选项名            |     作用      |  其他 |
|:------------------------:|:-----------:|----:|
| exception_log_file_path  | 异常信息保存文件路径  ||
|    version_file_path     |  版本信息文件路径   ||

## exception.log
保存程序异常，当程序运行时出现异常都会详细记录在该文件中，便于debug

## requirements.txt
保存程序运行时需要的第三方依赖。当程序检测到缺少依赖时会读取本文件并自动安装所需依赖

## font_dict.txt
保存思源黑体字体的字形信息的md5值和字符编码的映射，用于解决学习通的字体反爬

## version.json
保存程序更新信息和版本信息