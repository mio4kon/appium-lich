# -*- coding: utf-8 -*-

__author__ = 'Mio4kon'

from appium import webdriver
from base.action import ElementActions
from utils.environment import Environment

env = Environment().get_environment_info()
capabilities = {'platformName': env.devices[0].platform_name,
                'platformVersion': env.devices[0].platform_version,
                'deviceName': env.devices[0].device_name,
                'app': env.apk,
                'clearSystemFiles': True,
                'appActivity': env.app_activity,
                'appPackage': env.app_package,
                'automationName': 'UIAutomator2',
                'noSign': True,
                'newCommandTimeout': 60 * 100}
host = "http://localhost:4723/wd/hub"
driver = webdriver.Remote(host, capabilities)
action = ElementActions(driver)
