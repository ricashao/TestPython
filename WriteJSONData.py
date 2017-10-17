import os
import json
#向文件写入JSON数据
#fname 拖入的文件
#directory 要存储的文件路径
#data 数据
#returns 存储成功返回文件路径 存储失败返回null


def writeJson(fname, directory, data):
    if(os.path.exists(directory)):
        if(os.path.isdir(directory)):
            outpath = os.path.join(directory, fname + ".json");
            js = json.dumps(data, separators=(',', ':'), ensure_ascii=False);
            output = open(outpath, 'w+', buffering=2048)
            output.write(js)
            output.close()
            return outpath

#writeJSONData("test","//192.168.1.4/chuanqi.com/web/config/zhcn/trunk/raw","")