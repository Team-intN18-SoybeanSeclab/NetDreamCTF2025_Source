# 我最近刚开始学编程，随便写了一个pydoc生成器，希望能帮到大家。
# 欸？你说可以随便调用函数可能会导致安全问题？
# 什么嘛，pydoc里还能有RCE我的东西不成。
# 把魔术方法ban了就行了，pydoc能有多坏。真是的。

import pydoc

while True:
    func = input("please input a function in the pydoc package: ")
    if (func in dir(pydoc) 
        and callable(getattr(pydoc, func)) 
        and not func.startswith("__")
        and '.' not in func):
        args_string = input("please input arguments for the function (e.g. 123,456,789): ")
        args = [args_string for args_string in args_string.split(",")]
        if not args_string: print(getattr(pydoc, func)())
        else: print(getattr(pydoc, func)(*args))
    else:
        print("No hacker you can only use pydoc package functions")
