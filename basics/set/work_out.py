"""
set, 无序不重复
"""
s = {1,2,3}
s = set()
print(type(s))
s = {}  # 不要用空{}来初始化一个空set,因为这样得到的是一个空dict
print(type(s))

"""
add(1), 添加一个元素
update([1,2,3]) 添加多个元素
{1,2,3}.remove(3) 移除等于3的元素, 如果不存在会报错
{1,2,3}.discard(3) 移除等于3的元素, 不会报错   
union(), 合并两个set, 可以直接用 | 符号
s1.difference(s2), 返回s1中只属于s1的值的set, 用一个set表示, 也可以直接用减号
s1.symmetric_difference(s2), 返回s1,s2里面所有 非s1,s2共有的元素的set, 
"""
ss = {1,2,3} | {3,4,5}
print(ss)

