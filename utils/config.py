# -*- coding: utf-8 -*-
__author__ = 'Mio4kon'
from configparser import ConfigParser
import os
from utils import L


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


class Config:
    DEFAULT_CONFIG_DIR = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "data/config.ini")))
    BASE_PATH_DIR = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

    # titles:
    TITLE_NAME = "name"
    TITLE_ACCOUNT = "account"
    # values:
    # [name]
    VALUE_APP = "apk"
    VALUE_APP_ACTIVITY = "app_activity"
    VALUE_APP_PACKAGE = "app_package"
    # [account]
    VALUE_ACCOUNT_SUCCESS = "account_success"
    VALUE_PASSWORD_SUCCESS = "password_success"

    def __init__(self):
        self.path = Config.DEFAULT_CONFIG_DIR
        self.cp = ConfigParser()
        self.cp.read(self.path)
        L.i('初始化config...config path: ' + self.path)
        apk_name = self.get_config(Config.TITLE_NAME, Config.VALUE_APP)
        self.apk_path = Config.BASE_PATH_DIR + '/apk/' + apk_name
        self.xml_report_path = Config.BASE_PATH_DIR + '/report/xml'
        self.html_report_path = Config.BASE_PATH_DIR + '/report/html'
        self.pages_yaml_path = Config.BASE_PATH_DIR + '/page/yaml'
        self.env_yaml_path = Config.BASE_PATH_DIR + '/data/environment_info.yaml'
        self.app_activity = self.get_config(Config.TITLE_NAME, Config.VALUE_APP_ACTIVITY)
        self.app_package = self.get_config(Config.TITLE_NAME, Config.VALUE_APP_PACKAGE)
        self.account_success = self.get_config(Config.TITLE_ACCOUNT, Config.VALUE_ACCOUNT_SUCCESS)
        self.password_success = self.get_config(Config.TITLE_ACCOUNT, Config.VALUE_PASSWORD_SUCCESS)

    def set_config(self, title, value, text):
        self.cp.set(title, value, text)
        with open(self.path, "w+") as f:
            return self.cp.write(f)

    def add_config(self, title):
        self.cp.add_section(title)
        with open(self.path, "w+") as f:
            return self.cp.write(f)

    def get_config(self, title, value):
        return self.cp.get(title, value)

