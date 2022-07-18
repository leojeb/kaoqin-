import itertools
import operator

print('----accumulate----')
data = [1,2,3,4,5]
factorial_result = itertools.accumulate(data, operator.mul)
add_result = itertools.accumulate(data)
# operator包里有很多函数, 对应着python内置运算符, 这些函数就是为了有时将运算方法作为参数传入
"""
accumulate方法有点类似于scala的数据处理, 将第一个元素作为结果与第二个元素做运算, 然后将此运算结果与第三个元素做运算以此类推. 

"""
if operator.lt(1,2):
    print(1)

print('-----product-----')
l1 = [1,2,3]
l2 = ['a','b','c']
for i in itertools.product(l1,l2):
    print('type',type(i),'\t', i) # i是tuple类型的, 运行便知

colors = ['red', 'orange', 'yellow', 'green', 'blue']
alpha_colors, beta_colors, c_colors= itertools.tee(colors, 3)
for each in alpha_colors:
    print(each)
for each in beta_colors:
    print(each)
for each in c_colors:
    print(each)
