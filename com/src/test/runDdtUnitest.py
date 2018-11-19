#coding=utf-8

import unittest
import datetime
import os
from ddt import ddt,data
from com.src.test.tools import requestAction,getTestData,getLocustTestData
from com.src.test.HTMLTestRunner import HTMLTestRunner

@ddt
class DongManTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # cls.requestData = getTestData()
        pass

    @classmethod
    def tearDownClass(cls):
        pass


    @data(*getTestData())
    def test_InterfaceTest(self,values):
        # "%s" % values[8]
        # print(values,"###")
        # print(parseParams(values))
        result = requestAction(values)
        self.assertTrue(result)



if __name__ == "__main__":

    suite1 = unittest.TestLoader().loadTestsFromTestCase(DongManTestCase)
    suite = unittest.TestSuite([suite1
    ])
    date_now = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%doo%H%M%S')
    resport_path = os.path.abspath(os.path.join(os.path.pardir,"results%s系统测试报告%s.html" % (os.sep,date_now)))
    with open(resport_path,"wb") as f:
        runner = HTMLTestRunner(stream=f,title='测试报告',description='测试报告 详细信息')
        runner.run(suite)




