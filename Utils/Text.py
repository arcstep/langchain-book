import re

# 兼容带有某种属性的类或字典
def getter(obj, key):
    if isinstance(obj, dict):
        return obj.get(key, "")
    else:
        return getattr(obj, key, "")

# 移除base64编码
def remove_base64(content):
    pattern = r'base64,(?:(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?)'
    return re.sub(pattern, '', content)

# 移除示例代码中的输出结果
def remove_text_blocks(content):
    pattern = r'```text\r?\n.*?\r?\n```'
    return re.sub(pattern, '', content, flags=re.DOTALL)

# 按正则表达式过滤字典属性值，从字典、类等对象构成的列表中搜索
def search_from_list(dict_list, patten, key):
    new_dict_list = [obj for obj in dict_list if re.compile(patten, re.IGNORECASE).search(getter(obj, key))]
    resp = []
    for obj in new_dict_list:
        resp.append(obj)
    return resp

# 对字典、类等对象构成的列表按表示文档长度的键排序
def sort_list_by_len(dict_list, key):
    new_dict_list = [(obj, len(getter(obj, key))) for obj in dict_list]
    newDocs = sorted(new_dict_list, key = lambda x: x[1], reverse = True)
    return newDocs