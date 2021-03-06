# -*- coding: utf-8 -*-

#
# 带webdriver功能下载中间件起始类
# by wooght 2017-11
#

import io
import random
import sys
import time

import selenium
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options

import common.wfunc
from common.werror import Werror
from caijing_scrapy.settings import USER_AGENT, PHANTOMJSPAGES


# #代理
# from selenium.webdriver.common.proxy import Proxy
# from selenium.webdriver.common.proxy import ProxyType

class Wdownloadmiddlewares(object):
    save_error_pic = True  # 保存错误页面图片
    random_agent = False  # 随机agent
    disk_cache = False  # 启用浏览器缓存
    stdout_utf8 = False  # 输出缓冲编码
    timeout = 10  # 加载超时时间

    # 创建webdriver
    # 设置driver属性
    def set_cap_phantomjs(self):
        #  DesiredCapabilities指webdirver的环境
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        refererlist = [
            'http://www.baidu.com', 'http://www.qq.com', 'https://zhidao.baidu.com/'
        ]
        for key, value in PHANTOMJSPAGES.items():
            cap[key] = value
        cap['phantomjs.page.settings.userAgent'] = random.choice(USER_AGENT)
        if self.disk_cache:
            cap['phantomjs.page.settings.disk-cache'] = True
        if self.stdout_utf8:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码
        common.wfunc.e('phantomjs is ok')

        # 创建webdriver
        # #service_args中:--ssl-protocol=any具备访问加密请求https的功能
        self.driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'], desired_capabilities=cap)
        self.driver.maximize_window()  # 设置全屏
        self.driver.set_page_load_timeout(self.timeout)  # 设置超时时间

        self.driver.set_script_timeout(self.timeout * 2)  # 设置异步超时时间
        # self.driver.implicitly_wait(5)                    #设置只能等待时间

        common.wfunc.e('!+!+=new driver run=+!+!')


    # chromedriver
    def set_cap(self):
        # display = Display(visible=0, size=(1920, 1080))  # 构建虚拟窗口
        # display.start()
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 设置为无头的测试浏览器
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.maximize_window()
        common.wfunc.e('!+!+=new dirver run=+!+!')

    # 爬虫执行完后 余下操作
    def spider_closed(self):
        common.wfunc.e('driver closed')
        self.driver.quit()  # 关闭浏览器

    # 访问连接,浏览器解析连接response
    def open_url(self, url):
        # 动态设置agent
        if self.random_agent:
            self.driver.desired_capabilities['phantomjs.page.settings.userAgent'] = random.choice(USER_AGENT)
        try:
            common.wfunc.e('open url:' + url)
            t_one = time.time()
            self.driver.get(url)
            t_two = time.time()
            common.wfunc.e('spend times:' + str(t_two - t_one))
        except selenium.common.exceptions.TimeoutException as e:
            common.wfunc.e_error("Timeout")
            common.wfunc.e(e)
            if (self.save_error_pic):
                self.driver.save_screenshot('errpic/' + str(int(time.time())) + ".png")  # 保存报错图片
            raise Werror('...Timeout....')
        except Exception as e:
            common.wfunc.e_error('other error')
            common.wfunc.e(e)
            self.driver.quit()  # 退出旧的driver,减小内存
            self.set_cap()  # 10061错误,及phantomjs内容溢出,需重新启动
            raise ConnectionRefusedError()
            # self.set_proxy()

    # IP代理
    def set_proxy(self):
        proxy = webdriver.Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        proxy.http_proxy = random.choice(HTTP_IPS)
        # 将代理设置添加到webdriver.DesiredCapabilities.PHANTOMJS中
        proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
        self.driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)

    # 随机等待时间
    def delay(self):
        delay_time = random.randint(0, 2)
        # common.wfunc.e('delayd....' + str(delay_time))
        time.sleep(delay_time)
