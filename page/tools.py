# -*- coding: utf-8 -*-
__author__ = 'Mio4kon'
from utils import L
import yaml
import jinja2
from utils.environment import Environment

from utils.config import Config

pages_path = Environment().get_environment_info().pages_yaml


def parse():
    L.i('解析page.yaml, Path:' + pages_path)
    with open(pages_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


class GenPages:
    @staticmethod
    def gen_page_list():
        """
        将page.yaml转换成下面dict:
        :return: {'LoginPage': ['注册', '登录', '请输入手机号', '请输入验证码'], 'DebugPage': ['切换服务器', 'beta_http']}
        """
        _page_list = {}
        pages = parse()
        for page, value in pages.items():
            locators = value['locators']
            locator_names = []
            for locator in locators:
                locator_names.append(locator['name'])
            _page_list[page] = locator_names
        return _page_list

    @staticmethod
    def gen_page_py():
        """
        利用jinja2生成pages.py文件
        """
        base_dir = Config.BASE_PATH_DIR
        template_loader = jinja2.FileSystemLoader(searchpath=base_dir + "/page/template")
        template_env = jinja2.Environment(loader=template_loader)
        page_list = GenPages.gen_page_list()
        print(page_list)
        _templateVars = {
            'page_list': page_list
        }
        template = template_env.get_template("pages")
        with open(base_dir + '/page/pages.py', 'w', encoding='utf-8') as f:
            f.write(template.render(_templateVars))


if __name__ == '__main__':
    env = Environment().get_environment_info()
    print(env.pages_yaml)
