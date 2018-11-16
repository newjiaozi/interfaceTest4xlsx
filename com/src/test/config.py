#coding=utf-8


def getConfig():
    testcase_path = 'testcase.xlsx'
    testcase_name = '接口测试'  ## 命名sheet名称以及测试名称
    locust_min = 200
    locust_max = 4000
    # locust_host = "http://www.baidu.com"
    return {"testcase_path":testcase_path,"testcase_name":testcase_name,
            "locust_min":locust_min,"locust_max":locust_max}

