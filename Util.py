import os
import json
import xlrd
def getGlobalCfg(globalCfgPath):
    if(os.path.exists(globalCfgPath)):
        with open(globalCfgPath, 'r') as f:
            js = json.loads(f.read())
            return js
SHEET_EXTRA = "附加数据"
def parseExtraData(wb, fname, gcfg):
    pass

def getRemoteCfgs(path):
    if (os.path.exists(path)):
        with open(path, 'r',encoding="utf8") as f:
            js = json.loads(f.read())
            return js

#getRemoteCfgs("//192.168.1.4/chuanqi.com/web/config/zhcn/trunk/cfgs.json")