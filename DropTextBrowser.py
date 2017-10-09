from PyQt5.QtWidgets import QTextBrowser,QApplication,QWidget
import os
import sys
import xlrd
import json
class DropTextBroswer(QTextBrowser):
    def __init__(self, parent=None):
        super(DropTextBroswer,self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self,e):
        url = e.mimeData().urls()[0]
        suffix = os.path.splitext(url.toLocalFile())[1]
        if(suffix ==".xls" or suffix ==".xlsx"):
            e.accept()
        else:
            e.ignore()

    def dragLeaveEvent(self, e):
        pass

    def dragMoveEvent(self, e):
        pass

    def dropEvent(self, e):
        url = e.mimeData().urls()[0]
        excel_table(url.toLocalFile())

class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        button = DropTextBroswer(self)
        button.move(190, 65)

        self.setGeometry(300, 300, 600,300)
        self.setWindowTitle('简单拖放')


def excel_table(file='file.xls', colnameindex=0, ):
    filename = (os.path.split(file)[1]).split(".")[0]
    data = xlrd.open_workbook(file).sheet_by_index(0)
    flags = data.row_values(3)
    list = []
    for x in range(9, data.nrows ):
        tmp = []
        for y in range(1,data.ncols):
            if flags[y]:
                print(flags[y])
                print(data.cell(x,y))
                value = data.cell(x,y).value
                '''if isinstance(value, float):
                    tmp.append(value)
                elif isinstance(value, bytes):
                    print(value)
                    tmp.append(value.encode('utf-8'))
                else:
                    tmp.append(value)'''
                print(value)
                tmp.append(value)
        list.append(tmp)
    js = json.dumps(list,ensure_ascii=False);
    outputfile = filename + '.json'
    output = open(outputfile, 'w+', buffering=2048)
    output.write(js)
    output.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

