# -*- coding: utf-8 -*-


__author__ = 'Mio4kon'
import allure

from utils import L
from utils.environment import Environment


class Steps:
    @staticmethod
    @allure.step(title="获取账号和密码")
    def get_account():
        account = Environment().get_inited_config().account_success
        pwd = Environment().get_inited_config().password_success
        L.d('账号:%s 密码 %s' % (account, pwd))
        return [account, pwd]
