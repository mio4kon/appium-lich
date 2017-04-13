# -*- coding: utf-8 -*-
__author__ = 'Mio4kon'
import time


class Log:
    @staticmethod
    def e(msg, list_msg=[]):
        if list_msg:
            Log.show_list(msg, list_msg, Log.e)
        else:
            ColorLog.show_error(get_now_time() + " [Error]:" + "".join(msg))

    @staticmethod
    def w(msg, list_msg=[]):
        if list_msg:
            Log.show_list(msg, list_msg, Log.w)
        else:
            ColorLog.show_warn(get_now_time() + " [Warn]:" + "".join(msg))

    @staticmethod
    def i(msg, list_msg=[]):
        if list_msg:
            Log.show_list(msg, list_msg, Log.i)
        else:
            ColorLog.show_info(get_now_time() + " [Info]:" + "".join(msg))

    @staticmethod
    def d(msg, list_msg=[]):
        if list_msg:
            Log.show_list(msg, list_msg, Log.d)
        else:
            ColorLog.show_debug(get_now_time() + " [Debug]:" + "".join(msg))

    @staticmethod
    def show_list(msg, list_msg, f):
        temp = msg + "[ " + "\t".join(list_msg) + " ]"
        f(temp)



class ColorLog:
    @staticmethod
    def c(msg, colour):
        try:
            from termcolor import colored, cprint
            p = lambda x: cprint(x, '%s' % colour)
            return p(msg)
        except:
            print(msg)

    @staticmethod
    def show_verbose(msg):
        ColorLog.c(msg, 'white')

    @staticmethod
    def show_debug(msg):
        ColorLog.c(msg, 'blue')

    @staticmethod
    def show_info(msg):
        ColorLog.c(msg, 'green')

    @staticmethod
    def show_warn(msg):
        ColorLog.c(msg, 'yellow')

    @staticmethod
    def show_error(msg):
        ColorLog.c(msg, 'red')


def get_now_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
