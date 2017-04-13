# -*- coding: utf-8 -*-

__author__ = 'Mio4kon'
import time
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from utils import L
from exception.exceptions import *
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import TimeoutException


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class ElementActions:
    def __init__(self, driver: webdriver.Remote):
        self.driver = driver
        self.width = self.driver.get_window_size()['width']
        self.height = self.driver.get_window_size()['height']

    def reset(self, driver: webdriver.Remote):
        """因为是单例,所以当driver变动的时候,需要重置一下driver

        Args:
            driver: driver

        """
        self.driver = driver
        self.width = self.driver.get_window_size()['width']
        self.height = self.driver.get_window_size()['height']
        return self

    @staticmethod
    def sleep(s):
        return time.sleep(s)

    def back_press(self):
        self._send_key_event('KEYCODE_BACK')

    def dialog_ok(self, wait=5):
        locator = {'name': '对话框确认键', 'timeOutInSeconds': wait, 'type': 'id', 'value': 'android:id/button1'}
        self.click(locator)

    def set_number_by_soft_keyboard(self, nums):
        """模仿键盘输入数字,主要用在输入取餐码类似场景

        Args:
            nums: 数字
        """
        list_nums = list(nums)
        for num in list_nums:
            self._send_key_event('KEYCODE_NUM', num)

    def swip_left(self, count=1):
        """向左滑动,一般用于ViewPager

        Args:
            count: 滑动次数

        """
        for x in range(count):
            self.sleep(1)
            self.driver.swipe(self.width * 9 / 10, self.height / 2, self.width / 10, self.height / 2, 1500)

    def click(self, locator, count=1):
        """基础的点击事件

        Args:
            locator:定位器
            count: 点击次数
        """
        el = self._find_element(locator)
        if count == 1:
            self.sleep(1)

            el.click()
        else:
            touch_action = TouchAction(self.driver)
            try:
                for x in range(count):
                    touch_action.tap(el).perform()
            except:
                pass

    def get_text(self, locator):
        """获取元素中的text文本

        Args:
            locator:定位器
            count: 点击次数

        Returns:
            如果没有该控件返回None

        Examples:
            TextView 是否显示某内容
        """
        el = self._find_elements(locator)
        if el.__len__() == 0:
            return None
        return el[0].get_attribute("text")

    def text(self, locator, value, clear_first=False, click_first=True):
        """输入文本

        Args:
            locator: 定位器
            value: 文本内容
            clear_first: 是否先清空原来文本
            click_first: 是否先点击选中
        Raises:
            NotFoundElementError

        """
        if click_first:
            self._find_element(locator).click()
        if clear_first:
            self._find_element(locator).clear()
        self._find_element(locator).send_keys(value)

    def swip_down(self, count=1, method=None):
        """向下滑动,常用于下拉刷新

        Args:
            count: 滑动次数
            method: 传入的方法 method(action) ,如果返回为True,则终止刷新

        Examples:
            action.swip_down(count=100, method=lambda action: not action.is_key_text_displayed("暂无可配送的订单"))
            上面代码意思:当页面不展示"暂无可配送的订单"时停止刷新,即有单停止刷新
        """
        if count == 1:
            self.driver.swipe(self.width / 2, self.height * 2 / 5, self.width / 2, self.height * 4 / 5, 2000)
            self.sleep(1)
        else:
            for x in range(count):
                self.driver.swipe(self.width / 2, self.height * 2 / 5, self.width / 2, self.height * 4 / 5, 2000)
                self.sleep(1)
                try:
                    if method(self):
                        break
                except:
                    pass

    def is_toast_show(self, message, wait=20):
        """Android检查是否有对应Toast显示,常用于断言

        Args:
            message: Toast信息
            wait:  等待时间,默认20秒

        Returns:
            True 显示Toast

        """
        locator = {'name': '[Toast] %s' % message, 'timeOutInSeconds': wait, 'type': 'xpath',
                   'value': '//*[contains(@text,\'%s\')]' % message}
        try:
            el = self._find_element(locator, is_need_displayed=False)
            return el is not None
        except NotFoundElementError:
            L.w("[Toast] 页面中未能找到 %s toast" % locator)
            return False

    def is_text_displayed(self, text, is_retry=True, retry_time=5, is_raise=False):
        """检查页面中是否有文本关键字

        如果希望检查失败的话,不再继续执行case,使用 is_raise = True

        Args:
            text: 关键字(请确保想要的检查的关键字唯一)
            is_retry: 是否重试,默认为true
            retry_time: 重试次数,默认为5
            is_raise: 是否抛异常
        Returns:
            True: 存在关键字
        Raises:
            如果is_raise = true,可能会抛NotFoundElementError

        """

        try:
            if is_retry:
                return WebDriverWait(self.driver, retry_time).until(
                    lambda driver: self._find_text_in_page(text))
            else:
                return self._find_text_in_page(text)
        except TimeoutException:
            L.w("[Text]页面中未找到 %s 文本" % text)
            if is_raise:
                raise NotFoundTextError
            else:
                return False

    def is_element_displayed(self, locator, is_retry=True, ):
        """检查控件是否显示

        Args:
            is_retry:是否重试检查,重试时间为'timeOutInSeconds'
            locator: 定位器
        Returns:
            true:  显示
            false: 不显示
        """
        if is_retry:
            el = self._find_element(locator, is_need_displayed=True)
            return el is not None
        else:
            el = self._get_element_by_type(self.driver, locator)
            return el.is_displayed()

    # ======================= private ====================

    def _find_text_in_page(self, text):
        """检查页面中是否有文本关键字
        拿到页面全部source,暴力检查text是否在source中
        Args:
            text: 检查的文本

        Returns:
            True : 存在

        """
        L.i("[查找] 文本 %s " % text)
        return text in self.driver.page_source

    def _find_element(self, locator, is_need_displayed=True):
        """查找单个元素,如果有多个返回第一个

        Args:
            locator: 定位器
            is_need_displayed: 是否需要定位的元素必须展示

        Returns: 元素

        Raises: NotFoundElementError
                未找到元素会抛 NotFoundElementError 异常

        """
        if 'timeOutInSeconds' in locator:
            wait = locator['timeOutInSeconds']
        else:
            wait = 20

        try:
            if is_need_displayed:
                WebDriverWait(self.driver, wait).until(
                    lambda driver: self._get_element_by_type(driver, locator).is_displayed())
            else:
                WebDriverWait(self.driver, wait).until(
                    lambda driver: self._get_element_by_type(driver, locator) is not None)
            return self._get_element_by_type(self.driver, locator)
        except Exception as e:
            L.e("[element] 页面中未能找到 %s 元素" % locator)
            raise NotFoundElementError

    def _find_elements(self, locator):
        """查找多元素(不会抛异常)

        Args:
            locator: 定位器

        Returns:元素列表 或 []

        """
        if 'timeOutInSeconds' in locator:
            wait = locator['timeOutInSeconds']
        else:
            wait = 20

        try:
            WebDriverWait(self.driver, wait).until(
                lambda driver: self._get_element_by_type(driver, locator, False).__len__() > 0)
            return self._get_element_by_type(self.driver, locator, False)
        except:
            L.w("[elements] 页面中未能找到 %s 元素" % locator)
            return []

    @staticmethod
    def _get_element_by_type(driver, locator, element=True):
        """通过locator定位元素(默认定位单个元素)

        Args:
            driver:driver
            locator:定位器
            element:
                true:查找单个元素
                false:查找多个元素

        Returns:单个元素 或 元素list

        """
        value = locator['value']
        ltype = locator['type']
        L.i("[查找]元素 %s " % locator)
        if ltype == 'name':
            ui_value = 'new UiSelector().textContains' + '(\"' + value + '\")'
            return driver.find_element_by_android_uiautomator(
                ui_value) if element else driver.find_elements_by_android_uiautomator(ui_value)
        else:
            return driver.find_element(ltype, value) if element else driver.find_elements(ltype, value)

    def _send_key_event(self, arg, num=0):
        """
        操作实体按键
        Code码：https://developer.android.com/reference/android/view/KeyEvent.html
        Args:
            arg: event_list key
            num: KEYCODE_NUM 时用到对应数字

        """
        event_list = {'KEYCODE_HOME': 3, 'KEYCODE_BACK': 4, 'KEYCODE_MENU': 82, 'KEYCODE_NUM': 8}
        if arg == 'KEYCODE_NUM':
            self.driver.press_keycode(8 + int(num))
        elif arg in event_list:
            self.driver.press_keycode(int(event_list[arg]))
