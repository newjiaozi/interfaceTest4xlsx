#coding=utf-8

import urllib3
import sys
sys.path.append("E:\pycharm_projects\interfaceTest4xlsx")
from com.src.test.tools import getLocustTestData,parseParams
from com.src.test.logs import logger
import requests
import multiprocessing
from threading import Thread
import jsonpath
import time
import numpy as np

urllib3.disable_warnings()

class RunProcess():
    time_dict={}
    def getLocustData(self):
        parse_params_list = []
        locust_data = getLocustTestData()
        if locust_data:
            for i in locust_data:
                parse_params = parseParams(i)
                parse_params_list.append(parse_params)
            return parse_params_list

    def requestPost(self,url,data,headers,verify):
        urllib3.disable_warnings()
        resp = requests.post(url,data=data,headers=headers,verify=verify)
        return resp


    def requestGet(self,url,payload="",headers="",verify=False):
        urllib3.disable_warnings()
        logger.info(url)
        logger.info(payload)
        if "{" in url and "}" in url and payload:
            url_format = url.format(**payload)
            logger.info("转化后的url为：%s" % url_format)
            resp = requests.get(url,params=payload,headers=headers,verify=verify)
            return resp

    def actionTest(self,params_dict_list):      ##time_dict格式为{"key":[],"key2":[]}
        success_num = 0
        # time_list = {} ##格式为{"key":[],"key2":[]}
        for i in params_dict_list:
            logger.info(i)
            desc = i["desc"]
            if desc not in self.time_dict:
                logger.info("初始化time_list! %s " % desc)
                self.time_dict[desc]=[]
            if i["json"]:
                resp = self.requestPost(i["url"],i["json"],headers=i["headers"],verify=False)
            elif i["data"]:
                resp = self.requestPost(i["url"], i["data"],headers=i["headers"],verify=False)
            else:
                resp = self.requestGet(i["url"],i["payload"],headers=i["headers"],verify=False)
            self.time_dict[desc].append(resp.elapsed.total_seconds())
            logger.info("resp： %s" % resp.text)
            result = self.checkResult(resp,i)
            if result:
                success_num += 1
        if len(params_dict_list) == success_num:
            # logger.info("接口验证通过%s" % params_dict_list)
            return True
        else:
            logger.info("接口验证失败%s" % params_dict_list)
            return False


    def checkResult(self,resp,params_dict):
        result = False
        if resp and resp.ok:
            resp_json = resp.json()
            check_point = params_dict['checks']
            if check_point:
                pass_num = 0
                for p in check_point:
                    value = jsonpath.jsonpath(resp_json, p)  ##resp_json 为需要处理的json，p为json路径的jsonpath
                    if value:
                        if value[0] == check_point[p]:
                            pass_num += 1
                    else:
                        return result
                if len(check_point) == pass_num:
                    result = True
            return result
        else:
            return result

if __name__ == "__main__":
    rp = RunProcess()
    count = 1
    f_list = []
    for i in range(count):
        params_dict_list = rp.getLocustData()
        # logger.info(params_dict_list)
        # f = multiprocessing.Process(target=rp.actionTest,args=(params_dict_list,time_dict))
        f = Thread(target=rp.actionTest,args=(params_dict_list,))
        f_list.append(f)
        f.start()
    for i in range(count):
        f = f_list[i]
        f.join()

    logger.info("执行结束！")
    logger.info("time_dict！%s" % rp.time_dict)
    logger.info("共执行 %s 次操作" % count)
    for k,v in rp.time_dict.items():
        logger.info("%s : 平均响应时间为：%s ;中位数：%s;最长响应时间：%s;最短响应时间：%s;" % (k,np.mean(v),np.median(v),np.max(v),np.min(v)))






