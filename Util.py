import os
import json
import xlrd
def getGlobalCfg(globalCfgPath):
    cfg={}
    if(os.path.exists(globalCfgPath)):
        with open(globalCfgPath, 'r') as f:
            js = json.loads(f.read())
            return js
SHEET_EXTRA = "附加数据"
def parseExtraData(wb, fname, gcfg):
    pass