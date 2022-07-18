"""
keys(), values(), items() 方法
"""
print('----setdefault方法----')
dict1 = {1:2,3:4}
return_value = dict1.setdefault(4,5) # 如果字典里没有此key则添加此键值对并返回value的值, 如果有此key则直接返回对应的value
print(return_value)
print('-----合并dict------')
print({**{1:2,3:4}, **{5:6,7:8}})