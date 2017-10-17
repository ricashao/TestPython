from PyQt5.QtWidgets import QTextBrowser, QApplication, QWidget
import os
import sys
import xlrd
import json
import math
import Util
import TypeCheckers
import WriteJSONData


class DropTextBroswer(QTextBrowser):
    def __init__(self, parent=None):
        super(DropTextBroswer, self).__init__(parent)
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
        XLSXDecoder(js, url, "", "", "")
        # excel_table(url.toLocalFile())


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        button = DropTextBroswer(self)
        button.move(190, 65)

        self.setGeometry(300, 300, 600, 300)
        self.setWindowTitle('简单拖放')


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
        sfilePackage = cfgRow[4]  # parent;不处理没填的情况
        cSuper = cfgRow[5] or "";  # 前端基类
        sSuper = cfgRow[6] or "";  # 后端基类
        cInterfaces = []
        sInterfaces = []
        if (cfgRow[7]):
            cInterfaces = cfgRow[7].split(",")
        if (cfgRow[8]):
            sInterfaces = cfgRow[8].split(",")
        defines = {}

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
                                "checker": checker}
                if (col > max):
                    max = col;

        # 从第9行开始，是正式数据
        for row in range(dataRowStart, data.nrows):
            print(row)
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

                if(len(cRow)):
                    cdatas.append(cRow)
                if (len(sRow)):
                    sdatas.append(sRow)
        writeData(cdatas,sdatas,fname,gcfg)

def writeData(cdatas,sdatas,fname,gcfg):
    if len(cdatas):
        cpath = WriteJSONData.writeJson(fname.split(".")[0], gcfg["clientPath"], cdatas);

def excel_table(file):
    filename = (os.path.split(file)[1]).split(".")[0]
    data = xlrd.open_workbook(file).sheet_by_index(0)
    flags = data.row_values(3)
    types = data.row_values(6)
    list = []
    for x in range(9, data.nrows):
        tmp = []
        for y in range(1, data.ncols):
            if flags[y]:
                value = data.cell(x, y).value
                ctype = data.cell(x, y).ctype
                if (types[y] == "number" or (types[y] == "" and ctype == 2)):
                    value = value or 0;
                    if (value - math.floor(value)):
                        tmp.append(value)
                    else:
                        tmp.append(math.floor(value))
                elif isinstance(value, float):
                    tmp.append(value)
                elif isinstance(value, bytes):
                    tmp.append(value.encode('utf-8'))
                else:
                    tmp.append(value)
                print(value)
        list.append(tmp)
    js = json.dumps(list, separators=(',', ':'), ensure_ascii=False);
    outputfile = filename + '_bak.json'
    output = open(outputfile, 'w+', buffering=2048)
    output.write(js)
    output.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
