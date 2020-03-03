import functools 

numbers = [1,2,3,4]
result = map(lambda x: x + x, numbers)
#print(result)

list = [1,3,5,6,2]

print(functools.reduce(lambda a,b: a+b, list))