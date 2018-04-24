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
        return [None, self.addContent(key, interfaceDic, valueDic, regDic, pak, extlist)];


    # 添加内容
    def addContent(self,key, interfaceDic, valueDic, regDic, pak, extlist):
        added = False
        code = '''module core.game {
    export interface IConfigKey {     
        '''

        for k, v in interfaceDic.items():
            if k == key:
                added = True
            code += '''%s:string\n''' % (v)
        if not (added):
            code += '''%s:string;\n''' % (key)
        code += "\t}\n"
        added = False
        code += "\tConfigKey = {\n"

        for k, v in valueDic.items():
            if k == key:
                added = True
            code += '''\t\t%s: "%s",\n''' % (k, v)

        if not (added):
            code += '''\t\t%s: "%s",\n''' % (key, key)
        code +='''\t}
    function rP(key: string, CfgCreator: { new (): ICfg }, idkey: string = "id") {
    \tDataLocator.regCommonParser(key, CfgCreator, idkey);
    }
    function rE(key: string) {
    \tDataLocator.regExtra(key);
    }
    export function initData() {
    \tvar C = ConfigKey;
    \tvar P = %s;
    '''%(pak)

        added = False
        for k,v in regDic.items():
            if k==key:
                added = True
            idKey = ", " + v[1] if v[1] != "" else ""
            code += '''\trP(C.%s, %s%s);\n'''%(k,v[0],idKey)
        if not(added):
            code += '''\trP(C.%s, %sCfg);\n''' % (key, key)
        code += "\n"
        added = False
        #附加数据
        for k in extlist:
            code += '''rE(C.%s);\n'''%(k)
        #if not(added):
        #    code += '''\t\trE(C.%s);\n''' % (key)
        code += '''\t}
}'''
        print(code)
        return code


#client = ClientRegTemplate()
#client.addToFile("F:\workspace\client\Client\src\chuanqi\GConfig.ts", "test", "")
