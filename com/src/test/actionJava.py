from jpype import *
import os.path



def encpwByJava(id,pwd,sessionKey,eValue,nValue):
    jarpath = os.path.abspath(os.path.join(os.path.abspath('.'), "..","java","Rsa.jar"))
    startJVM(getDefaultJVMPath (),'-ea', "-Djava.class.path=%s" % jarpath)
    JD = JClass("Rsa")
    res = JD.getEncpw(id,pwd,sessionKey,eValue,nValue)
    print(res)
    shutdownJVM()
    return res