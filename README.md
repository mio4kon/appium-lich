# Environment

## Python3:
    安装Python3
    brew install python3
    
    安装以下:pip3 install <name>

* Appium-Python-Client
* Jinja2
* PyYAML
* pytest
* pytest-allure-adaptor
* watchdog
* termcolor  (not needed)

## Appium 

	npm install -g appium
	npm install -g appium-doctor

`appium-doctor` to ensure your system is set up properly

[more](https://github.com/appium/appium)

## Allure-Commandline

**Allure Framework** is a flexible lightweight multi-language test report tool with the possibility to add screenshots, logs and so on. It provides modular architecture and neat web reports with the ability to store attachments, steps, parameters and many more. 

	brew tap qatools/formulas 
	brew install allure-commandline


**TODO**:  use Jenkins Plugin  

[more](https://github.com/allure-framework/allure1/wiki)

# Run Test

start appium service:
	
	appium --address 127.0.0.1 --port 4723 --log "log_path" --log-timestamp --local-timezone --session-override
	
run test:

	cd project_path
	python3 run.py

**Html-Report** will be generate on `project_path/report/html/index.html`

report shot:

![](screenshot/report_shot.jpeg)



# Write Test Case

## 开启watchdog

	cd project_path
	python3 watch_dog.py

打开 `project_path/data/pages.yaml`,以下面模板定位元素:

```xml

---
LoginPage:
  dec: 登录页面
  locators:
    -
      name: 注册
      timeOutInSeconds: 20
      type: name
      value: 注册
```

`LoginPage` : 主要标识元素所属页面 (名自取)   
`dec`:描述页面(爱写不写)  
`locators - name`: 代码会用此名称定位元素(名自取)  
`locators - timeOutInSeconds`: 超时时间,重试查找时间  
`locators - type`: 定位元素方式(id,name,xpath,class name等)  
`locators - value`:定位元素的值 (通过uiautomatorviewer等方式确认)

`watchdog`的作用是用来监听此`yaml`文件的变化,没当保存一次后会生成代码到 `project_path/page/pages.py`中,方便之后使用.

## 写测试case

	cd project_path/test/
	vi xxx_test

编写内容请仿造示例.下面会说明几个关键点:

* `action` 与 `action2`

**两者在测试方法中都可以通过参数接收使用**

`project_path/test/conftest.py`中包含`action`和`action2`区别在于:

`action` : 作用域是`class`,`class`中的方法全部按顺序执行完后会走`yield`后的代码.也就是关闭APP

`action2`: 作用域是`function`,`class`中的每一个方法执行完都会走`yield`后的代码.也就是关闭APP

**例**: `home_test.py` , `login_test.py`

[相关文档](http://doc.pytest.org/en/latest/fixture.html#fixtures)


* `data/config.ini`
	
	path下的内容**不需要**改  
	account下的内容是账号的配置可以改  
	如果想增加配置可**参考源码**实现或者**找我啊**
	
* `data/environment_info.yaml`

	自动生成的内容包含测试运行的环境.不用改!

* 每个操作之间如果为了确保不会因为手机卡顿或其他原因,请为了保障case通过率,多使用`sleep`


# TODO

* 兼容iOS
* 集成 [stf](https://github.com/openstf/stf)

