#coding=utf-8



import time
import webbrowser
import subprocess
from com.src.test.tools import *


if __name__ == "__main__":
    logger = get_logger()
    random_port = getRandomPort()
    logger.info("获取随机Locust PORT:%s" % random_port)
    p = subprocess.Popen("locust -f locustAction.py -P %s --web-host=127.0.0.1" % random_port)
    # logger.info(p.read())
    time.sleep(3)
    webbrowser.open("http://127.0.0.1:%s" % random_port,new=1,autoraise=True)
    p.wait()