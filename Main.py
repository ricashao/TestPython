from mainwindow import Ui_MainWindow  # 导入uitestPyQt5.ui转换为uitestPyQt5.py中的类

from PyQt5 import QtWidgets
import os
import sys
import xlrd
import Util
import TypeCheckers
import WriteJSONData
from datetime import datetime
import MenualCodeHelper
from ClientRegTemplate import ClientRegTemplate

# 全局变量
defines = {}


class Main(QtWidgets.QMainWindow, Ui_MainWindow):
    # 建立的是Main Window项目，故此处导入的是QMainWindow
    # 参考博客中建立的是Widget项目，因此哪里导入的是QWidget
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        url = e.mimeData().urls()[0]
        suffix = os.path.splitext(url.toLocalFile())[1]
        if (suffix == ".xls" or suffix == ".xlsx"):
            e.accept()
        else:
            e.ignore()

    def dragLeaveEvent(self, e):
        pass

    def dragMoveEvent(self, e):
        pass

    def dropEvent(self, e):
        url = e.mimeData().urls()[0]
        filePath = os.path.split(url.toLocalFile())[0]
        globalCfgPath = os.path.normpath(os.path.join(filePath, os.pardir, "globalConfig.json"))
        js = Util.getGlobalCfg(globalCfgPath)
        if ("remote" in js):
            js = Util.getGlobalCfg(js["remote"])
        cPath = self.txtClientPath.text();
        sPath = self.txtServerPath.text();
        XLSXDecoder(js, url, cPath, sPath, "")


class XLSXDecoder(object):
    def __init__(self, gcfg, file, cPath, sPath, cb):
        cPath = cPath or "";
        sPath = sPath or "";
        file = file.toLocalFile()
        fname = os.path.basename(file)
        rowCfgs = {
            "支持的数据类型": None,
            "程序配置说明": None,
            "程序配置内容": "cfgRow",
            "前端解析": "clientRow",
            "后端解析": "serverRow",
            "默认值": "defaultRow",
            "数据类型": "typeRow",
            "描述": "desRow",
            "属性名称": "nameRow"
        }

        data = xlrd.open_workbook(file).sheet_by_index(0)
        # 数据起始行
        dataRowStart = 0;
        rowCfgLines = {};
        # 先遍历所有行，直到得到"属性名称"行结束
        colData = data.col_values(0);
        for i in range(0, data.nrows):
            key = colData[i]
            if (key in rowCfgs):
                rowCfgLines[rowCfgs[key]] = i;
                if (rowCfgs[key] == "nameRow"):
                    dataRowStart = i + 1
                    break
        # 配置列
        cfgRow = data.row_values(rowCfgLines["cfgRow"]);
        if (cfgRow == None):
            print("表的配置有误，没有\"程序配置内容\"这一行")
            return  # return cb(file, true)

        # 先处理附加数据
        # hasExtra = Util.parseExtraData(data, fname.split(".")[0], gcfg);

        cfilePackage = cfgRow[3]  # parent;不处理没填的情况
        # print("cfilePackage"+cfilePackage)
        sfilePackage = cfgRow[4]  # parent;不处理没填的情况
        cSuper = cfgRow[5] or "";  # 前端基类
        sSuper = cfgRow[6] or "";  # 后端基类
        cInterfaces = []
        sInterfaces = []
        if (cfgRow[7]):
            cInterfaces = cfgRow[7].split(",")
        if (cfgRow[8]):
            sInterfaces = cfgRow[8].split(",")
        defines.clear()

        cdatas = []
        sdatas = []
        # 前端是否解析此数据
        clientRow = data.row_values(rowCfgLines["clientRow"]);
        # 后端是否解析此数据
        serverRow = data.row_values(rowCfgLines["serverRow"]);
        defaultRow = data.row_values(rowCfgLines["defaultRow"]) or [];
        # 类型列
        typeRow = data.row_values(rowCfgLines["typeRow"]);
        # 描述列
        desRow = data.row_values(rowCfgLines["desRow"]);
        # 属性名称列
        nameRow = data.row_values(rowCfgLines["nameRow"]);
        max = 0;
        checkers = TypeCheckers.checkers;
        for key in range(len(nameRow)):
            col = +key
            if (col != 0):
                client = +int(clientRow[col] or 0);
                server = +int(serverRow[col] or 0);
                type = typeRow[col] or "";
                checker = checkers[type];
                desc = "" + desRow[col];
                name = "" + nameRow[col];
                default = defaultRow[col];
                defines[col] = {"client": client, "server": server, "name": name, "desc": desc, "default": default,
                                "checker": checker, "type": type}
                if (col > max):
                    max = col;

        # 从第9行开始，是正式数据
        for row in range(dataRowStart, data.nrows):
            # print(row)
            rowData = data.row_values(row)
            col1 = rowData[0]
            # if ~col1or col1.charAt(0) != "!":
            # 先做空行检查，减少误报信息
            flag = False;
            for col in range(1, max + 1):
                cell = rowData[col];
                if (col in defines):
                    df = defines[col]
                    if df["client"] or df["server"]:
                        flag = True;
                        break;
            if flag:
                cRow = []
                sRow = []
                for col in range(1, max + 1):
                    try:
                        if (col in defines):
                            df = defines[col]
                            cell = rowData[col]
                            tmp = dir(df["checker"])
                            dat = df["checker"].check(cell or "");
                            if df["client"]:
                                cRow.append(dat)
                            if df["server"]:
                                sRow.append(dat)
                        else:
                            continue;
                    except Exception as err:
                        print("解析{0}第{1}行，第{2}列数据有误：{3}", fname, row + 1, col, err.message)

                if (len(cRow)):
                    cdatas.append(cRow)
                if (len(sRow)):
                    sdatas.append(sRow)
        writeData(cdatas, sdatas, fname, gcfg, cSuper, sSuper, cfilePackage, sfilePackage, cPath, sPath, cInterfaces,
                  sInterfaces)


def writeData(cdatas, sdatas, fname, gcfg, cSuper, sSuper, cfilePackage, sfilePackage, clientPath, serverPath,
              cInterfaces, sInterfaces):
    #print("cSuper:" + cSuper)
    fname = fname.split(".")[0]
    if len(cdatas):
        cpath = WriteJSONData.writeJson(fname, gcfg["clientPath"], cdatas);
        if cpath:
            print("文件%s，将客户端数据保存至：%s" % (fname, cpath))
        else:
            print("文件%s，未将客户端数据保存到：%s,请检查" % (fname, cpath))

    cPros = ""
    cDecode = ""
    cout = ""
    hasClocal = False
    for k in defines:
        define = defines[k]
        checker = define["checker"]
        pro = '''
        \t\t\t/**
        \t\t\t*%s
        \t\t\t**/
        \t\t\tpublic %s:%s
        ''' % (define["desc"], define["name"], define["type"])
        # print(pro)
        decode = ""
        default = ""
        if define["default"]:
            default = define["default"]
        decode = "\t\t\t@target@.%s = data[i++]%s\n" % (define["name"], "||" + default if default else"")
        # print(decode)
        client = define["client"]
        tmp = ""
        if client:
            if client == 1:
                cPros += pro
                tmp = decode.replace("@target@", "this")
            elif client == 2:
                hasClocal = True
                tmp = decode.replace("@target@", "local")
            cDecode += tmp
    # temp path todo
    path = os.path.join(clientPath + cfilePackage, fname + "Cfg.ts")
    cdict = MenualCodeHelper.getManualCodeInfo(path);
    createTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 生成客户端代码
    if cPros:
        cout = '''module lingyu.%s{
        %s
         /**
        * 由junyouH5数据生成工具，从%s生成
        * 创建时间：%s
        **/
         export class %sCfg%s%s {
         %s
         %s
         public decode(data:any[]){
         \t\t\tlet i = 0;
             %s
             %s
             %s
            }
        }
         %s
    }
        ''' % (gcfg["project"], MenualCodeHelper.genManualAreaCode("$area1", cdict), cpath, createTime, fname,
               " extends" + cSuper if cSuper else "",
               " implements " + (",".join(cInterfaces)) if len(cInterfaces) else "", cPros,
               MenualCodeHelper.genManualAreaCode("$area2", cdict),
               "\t\t\tlet local:any = {};" if hasClocal else "",
               cDecode, MenualCodeHelper.genManualAreaCode("$decode", cdict),
               MenualCodeHelper.genManualAreaCode("$area3", cdict))
    saveCodeFile(clientPath, cfilePackage, cout, fname + "Cfg")
    #尝试生成注册文件
    if (clientPath and cout and gcfg["clientRegClass"]):
        clientReg = ClientRegTemplate();
        [cerr,crout] = clientReg.addToFile(os.path.join(clientPath, gcfg["clientRegClass"][1]+"/"+ gcfg["clientRegClass"][0] + ".ts"),fname,"lingyu."+gcfg["project"])
        if (cerr) :
            print(cerr);
        else:
            saveCodeFile(clientPath, "/"+gcfg["clientRegClass"][1], crout, gcfg["clientRegClass"][0]);

def saveCodeFile(dir, filePackage, content, fname):
    if not (content):
        return
    if (dir and filePackage):
        fname += ".ts"
        dir = dir.replace('\\','/')
        fullPath = dir+filePackage
        if fullPath:
            if os.path.exists(fullPath):
                if os.path.isdir(fullPath):
                    file = os.path.join(fullPath,fname)
                    output = open(file, 'w+', buffering=2048,encoding='utf8')
                    output.write(content)
                    output.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
