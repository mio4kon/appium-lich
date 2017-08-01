# -*- coding: utf-8 -*-

__author__ = 'Mio4kon'

import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from page.tools import GenPages
from utils import L
from utils.environment import Environment


def gen_page_py():
    GenPages.gen_page_py()


class WatchHandler(PatternMatchingEventHandler):
    patterns = ["*.yaml"]

    def on_modified(self, event):
        L.i('监听到文件: yaml 发生了变化')
        try:
            gen_page_py()
        except Exception as e:
            L.e('\n!!!!!!!---pages.yaml---!!!!!!\n解析文件 pages.yaml 错误\n'
                '请到{}路径下检查修改后重新保存.'.format(self.watch_path))


if __name__ == "__main__":
    event_handler = WatchHandler()
    full_path = Environment().get_environment_info().pages_yaml
    print(full_path)
    observer = Observer()
    observer.schedule(event_handler, full_path)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
