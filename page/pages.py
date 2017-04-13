# -*- coding: utf-8 -*-
__author__ = 'Mio4kon'
from page import tools

pages = tools.parse()


def get_locater(clazz_name, method_name):
    locators = pages[clazz_name]['locators']
    for locator in locators:
        if locator['name'] == method_name:
            return locator


class HomePage:
    登录入口 = get_locater('HomePage', '登录入口')

    
class LoginPage:
    账户 = get_locater('LoginPage', '账户')
    密码 = get_locater('LoginPage', '密码')
    登录 = get_locater('LoginPage', '登录')

    



