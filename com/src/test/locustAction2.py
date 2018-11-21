#coding=utf-8


from locust import task,HttpLocust,TaskSet
import sys
sys.path.append("E:\pycharm_projects\interfaceTest4xlsx")
print(sys.path)
from com.src.test.config import getConfig
from com.src.test.tools import getLocustTestData,parseParams
from com.src.test.logs import logger




class UserBehavior(TaskSet):

    def on_start(self):
        pass

    @classmethod
    def getLocustData(self):
        parse_params_list = []
        locust_data = getLocustTestData()
        if locust_data:
            for i in locust_data:
                parse_params = parseParams(i)
                parse_params_list.append(parse_params)
            # logger.info(parse_params)
            return parse_params_list

    def requestPost(self,url,data):
        logger.info(url)
        logger.info(self.client.post(url,data))
        with self.client.post(url,data,catch_response = True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Failed")

    def requestGet(self,url,payload=""):
        logger.info(url)
        logger.info(payload)
        if "{" in url and "}" in url and payload:
            url_format = url.format(**payload)
            logger.info("转化后的url为：%s" % url_format)
            logger.info(self.client.get(url_format))
            with self.client.get(url_format,catch_response = True) as response:
                if response.status_code == 200:

                    response.success()
                else:
                    response.failure("Failed")
        else:
            logger.info(self.client.get(url))
            with self.client.get(url,catch_response = True) as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure("Failed")

    @task()
    def actionTest(self):
        params_dict_list = self.getLocustData()
        logger.info(params_dict_list)
        for i in params_dict_list:
            logger.info(i)
            if i["json"]:
                self.requestPost(i["path_url"],i["json"])
            elif i["data"]:
                self.requestPost(i["path_url"], i["data"])
            else:
                self.requestGet(i["path_url"],i["payload"])


class WebsiteUser(HttpLocust):
    params_dict_list = UserBehavior.getLocustData()
    task_set = UserBehavior
    cf = getConfig()
    host = params_dict_list[0]['host_url']
    min_wait = cf["locust_min"]
    max_wait = cf["locust_max"]



