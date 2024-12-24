import pandas
import json
import os


# tools in python. just ignore them. 在python中使用的小工具，无视即可

def get_list_depth(lst):
    if isinstance(lst, list):
        return 1 + max(get_list_depth(item) for item in lst)
    else:
        return 0

def read_str(data,null):
    if pandas.isnull(data):
        return null
    else:
        return data

def language_fill(list_language,df):
    #language fill
    for i in df.columns:
      if not i in list_language:
         print("wrong language code:{0}, please check\n语言代码：{0}有问题，请检查csv_other_loc".format(i))
    if 'english' in df.columns:
        for i in list_language:
            if not i in df.columns:
                df[i] = df['english']
    else:
        for i in list_language:
            if not i in df.columns:
                df[i] = df.iloc[:,0]
    return df

# 读取并解析JSON数据，如果失败则使用默认值
# Read and parse JSON data, use default values if failed
def load_json(series, column, default, data_name, key):
    try:
        return json.loads(series[column])
    except Exception as e:
        print("{}: Read {} failed. 读取\"{}\"数据失败。（{}）".format(key, column, column, data_name))
        print(e)
        return default

# 创建目录的函数
# Function to create directories
def create_dir(path):
    try:
        os.mkdir(path)
    except:
        pass