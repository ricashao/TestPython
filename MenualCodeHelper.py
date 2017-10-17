import os
import re

ManualCodeDefaultComment = {
    # 类上方提示
    "$area1": "//这里填写类上方的手写内容",
    # 类中提示
    "$area2": "//这里填写类里面的手写内容",
    # 类下方提示
    "$area3": "//这里填写类下发的手写内容",
    # 处理函数提示
    "$decode": "//这里填写方法中的手写内容"
}


def getManualCodeInfo(file):
    dict = {}
    if (os.path.exists(file)):
        with open(file, 'r', encoding="utf8") as f:
            content = f.read();
            reg = re.compile(r'[/][*]-[*]begin[ ]([$]?[a-zA-Z0-9]+)[*]-[*][/]([\s\S]*)[/][*]-[*]end[ ]\1[*]-[*][/]')
            result = re.findall(reg, content)
            #print(result)
            if result and len(result):
                for k,v in result:
                    #print(k,v)
                    manual = str(v).strip()
                    if not(v):
                        continue;
                    elif k in ManualCodeDefaultComment:
                        if(ManualCodeDefaultComment[k] == manual):
                            continue;
                        dict[k] = v;
    return dict

#生成手动代码区域的文本
def genManualAreaCode(key, cinfo):
    if key in cinfo:
        manual = cinfo[key]
    else:
        if key in ManualCodeDefaultComment:
            manual = ManualCodeDefaultComment[key]
        else:
            print("错误的区域标识"+key)
    return '''
        /*-*begin %s*-*/
        %s
        /*-*end %s*-*/
    '''%(key,manual,key)

def test():
    print(re.match(r'^\d{3}\-\d{3,8}$', '010-123459'))


# test()
#getManualCodeInfo("F://mygit/TestPython/jsons/ShouChongCfg.ts")
