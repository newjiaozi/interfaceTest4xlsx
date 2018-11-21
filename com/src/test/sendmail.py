#coding=utf-8

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import time
import os
from com.src.test.logs import logger
from com.src.test.tools import getRunningINI
import zipfile

class EmailClass():
    def __init__(self):

        self.curDateTime = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())) #当前日期时间
        self.sender = getRunningINI("sender","email","static.ini","utf-8")# 从配置文件获取，发件人
        self.msg_title = getRunningINI("title","email","static.ini","utf-8") #从配置文件获取，邮件标题
        self.sender_server =getRunningINI("server","email","static.ini","utf-8") #从配置文件获取，发送服务器
        self.To = getRunningINI("receiver","email","static.ini","utf-8")
        self.passwd = getRunningINI("passwd","email","static.ini","utf-8")

    '''
    配置邮件内容
    '''
    def setMailContent(self):
        msg = MIMEMultipart()
        msg['Subject'] = Header('%s%s'%(self.msg_title,self.curDateTime),'utf-8')
        msg.attach(MIMEText('测试报告见附件', 'plain', 'utf-8'))

        #附件路径
        zipfiles_dst_path = os.path.join(os.path.dirname(__file__), "..",'results.zip')
        if os.path.exists(zipfiles_dst_path):
            os.remove(zipfiles_dst_path)
            # logger.info("移除文件%s成功" % zipfiles_dst_path)
        zipfiles_dst = zipfile.ZipFile(zipfiles_dst_path, 'w')
        zipfiles_src = os.path.join(os.path.dirname(__file__), "..",'results')

        pre_len = len(os.path.dirname(zipfiles_src))
        # logger.info(pre_len)
        for parent, dirnames, filenames in os.walk(zipfiles_src):
            # logger.info(parent)
            # logger.info(dirnames)
            # logger.info(filenames)
            for filename in filenames:
                pathfile = os.path.join(parent,filename)
                arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
                # logger.info(pathfile)
                # logger.info(arcname)
                zipfiles_dst.write(pathfile, arcname)
        zipfiles_dst.close()

        #增加附件
        # 构造附件
        att1 = MIMEText(open(zipfiles_dst_path, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename="result.zip"'
        msg.attach(att1)
        return msg


    '''
    发送电子邮件
    '''
    def sendEmail(self):
        try:
            msg = self.setMailContent()
            smtpObj = smtplib.SMTP()
            # smtpObj.set_debuglevel(1)
            smtpObj.connect(self.sender_server,25)
            smtpObj.login(self.sender,self.passwd)
            smtpObj.sendmail(self.sender,self.To ,msg.as_string())
            smtpObj.quit()
            logger.info("邮件发送成功")
            zipfiles_dst_path = os.path.join(os.path.dirname(__file__), "..", 'results.zip')
            if os.path.exists(zipfiles_dst_path):
                os.remove(zipfiles_dst_path)
                # logger.info("移除文件%s成功" % zipfiles_dst_path)
            time.sleep(2)
            # self.deleteFiles()
        except smtplib.SMTPException as ex:
            logger.error("Error: 无法发送邮件.%s"%ex)


    def deleteFiles(self):
        res = os.path.join(os.path.dirname(__file__), "..", 'results')
        # logger.info("即将删除文件所在目录 %s" % res)
        for i,j,k in os.walk(res):
            for ks in k:
                file_name = os.path.join(i,ks)
                if os.path.isfile(file_name):
                    # logger.info(file_name)
                    # logger.info(os.path.splitext(file_name))
                    if os.path.splitext(file_name)[1] in [".xlsx",".html"]:
                        os.remove(file_name)


if __name__=="__main__":
    ec = EmailClass()
    ec.sendEmail()
