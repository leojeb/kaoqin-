
list1 = [1, 2, 3]
print('-----列表截取------')
print(list1[:])
print(list1[1:])
print(list1[-5:-1])  # 注意这里负数时的输出, 从-5到-1, 左开右闭
print(list1[-1:])  # 从-1到0, 左开右闭

print(len(list1))

# list合并和复制
print('------串联和复制-------')

print([1, 2, 3] + [1, 3, 2])
print([1, 2] * 3)
# 删除元素
print('------删除元素-------')
list2 = [1, 2, 3]
del list2[0]
print(list2)

print('------遍历--------')
for i, ele in enumerate(list1):
    print('第{}位是{}'.format(i, ele))

print('---------一次性遍历多个数组---------')
for a, b in zip(list1, ['a', 'b', 'c']):
    print('{}对应{}'.format(a, b))

print('-----判断---- \n in 和 not in')
print('----将列表元素一次性赋值给多个变量------')
a, b, c = [1, 2, 3]
print(a, b, c)

print('---列表也可以用自增、自乘运算符---')
list3 = [1, 2, 3]
list3 += ['world']
list3 *= 2
print(list3)

print('------index, append, insert方法-----')
print([1,2].index(1))
l = [1,2]
l.append(2)
print(l)
l.insert(0,'word')
print(l)
"""
pop(), pop(i), 移出列表最后一个/第i个元素, 并将其作为返回值返回
其他的直接cheatsheet找吧
"""
