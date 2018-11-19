#coding=utf-8


from locust import task,HttpLocust,TaskSet
import sys
sys.path.append("E:\pycharm_projects\interfaceTest4xlsx")
print(sys.path)
from com.src.test.config import getConfig
from com.src.test.tools import getLocustTestData,parseParams,get_logger




class UserBehavior(TaskSet):

    @classmethod
    def getLocustData(self):
        locust_data = getLocustTestData()
        if locust_data:
            parse_params = parseParams(locust_data[0])
            # logger.info(parse_params)
            return parse_params

    def requestPost(self,url,data):
        logger = get_logger()
        logger.info(url)
        logger.info(self.client.post(url,data))
        return self.client.post(url,data)

    def requestGet(self,url,payload=""):
        logger = get_logger()
        logger.info(url)
        logger.info(payload)
        if "{" in url and "}" in url and payload:
            url_format = url.format(**payload)
            logger.info("转化后的url为：%s" % url_format)
            logger.info(self.client.get(url_format))
            return self.client.get(url_format)
        else:
            logger.info(self.client.get(url))
            return self.client.get(url)

    @task()
    def actionTest(self):
        params_dict = self.getLocustData()
        if params_dict["json"]:
            self.requestPost(params_dict["path_url"],params_dict["json"])
        elif params_dict["data"]:
            self.requestPost(params_dict["path_url"], params_dict["data"])
        else:
            self.requestGet(params_dict["path_url"],params_dict["payload"])


class WebsiteUser(HttpLocust):
    params_dict = UserBehavior.getLocustData()
    task_set = UserBehavior
    cf = getConfig()
    host = params_dict['host_url']
    min_wait = cf["locust_min"]
    max_wait = cf["locust_max"]




