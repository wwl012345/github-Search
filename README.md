# github-Search
使用关键字匹配，可以对github中的公司资产、敏感信息进行搜索排查。

### 一、配置文件
1.修改配置文件info.ini，在里面填写自己的github的账号及密码(这样可以搜索更多的内容)
2.填写KEYWORDS，KEYWORDS中填写需要搜索的公司(如百度)，可以填写多个
3.填写PAYLOADS，里面填写需要搜索的关键字(如password)，可以填写多个
4.然后通过一一遍历，对KEYWORDS和PAYLOADS进行匹配

### 二、使用方法
命令行执行:

python3 GitHub.py
<img width="1425" alt="image" src="https://user-images.githubusercontent.com/53456907/155297520-0e7fc12c-de5f-460f-85aa-ee0fdb6eb372.png">


### 三、输出结果
直接在命令行中输出，如果需要，可以自行输出到文件中
