import os
import re

CConfigKeyReg = r'export\s*interface\s*IConfigKey\s*[{]([\s\S]*)[}]'
CConfigItem = r'([/][*][^]+?[*][/])?\s+([a-zA-Z_0-9]+)\s*:\s*string;'
CValueItem = r'([a-zA-Z_0-9]+)\s*:\s*"([a-zA-Z_0-9]+)"'
regCfg = r'rP[(]C[.]([a-zA-Z_0-9]+)\s*,\s*([a-zA-Z_0-9.]+)(?:\s*,\s*("[a-zA-Z_0-9.]+"))?[)];'
extCfg = r'rE[(]C[.]([a-zA-Z_0-9]+)[)];'


class ClientRegTemplate(object):
    def addToFile(self, file, key, pak):
        interfaceDic = {}
        valueDic = {}
        regDic = {}
        extlist = []

        if (not (os.path.exists(file) or not (os.path.isfile(file)))):
            return
        with open(file, 'r', encoding="utf8") as f:
            content = f.read()
        # print(CConfigKeyReg)
        reg = re.compile(CConfigKeyReg)
        resCk = re.findall(reg, content)
        # 检查ConfigKey常量
        if resCk:
            cfgs = resCk[0];
            reg = re.compile(CConfigItem)
            res = re.findall(reg, cfgs)
            if res:
                for tuple1 in res:
                    interfaceDic[tuple1[1]] = tuple1[1]
                    # print(interfaceDic)

        reg = re.compile(CValueItem)
        res = re.findall(reg, content)
        if res:
            for tuple1 in res:
                valueDic[tuple1[0]] = tuple1[1]
                # print(valueDic)

        reg = re.compile(regCfg)
        res = re.findall(reg, content)
        if res:
            for tuple1 in res:
                regDic[tuple1[0]] = [tuple1[1], tuple1[2]];
                # print(regDic)

        reg = re.compile(extCfg)
        res = re.findall(reg, content)
        if res:
            extlist = res
        return [None, addContent(key, interfaceDic, valueDic, regDic, pak, extlist)];

#添加内容
def addContent(key, interfaceDic, valueDic, regDic, pak, extlist, hasExtra):
    added = False
    code = '''module lingyu.game {
        \texport interface IConfigKey {
        
    '''
    for k,v in interfaceDic:
        if k == key:
            added = True
        code +='''\t\t%s\n'''%(v)
        if not(added):
            code += '''\t\t%s: string;\n'''%(k)
    code += "\t}"

    print(code)
client = ClientRegTemplate()
client.addToFile("F:\workspace\client\Client\src\chuanqi\GConfig.ts", "", "")
