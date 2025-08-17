# 上次可恶的嘿课把我沙箱打烂了，你们太坏了。
# 预热题到这里结束，我们正赛再见。玩得开心！
# 我超这预热题怎么这么坏啊！！！！！呜呜呜，再也CTF不起来了。
# Hint0：https://www.bilibili.com/video/BV163tYeQEuv/
# Hint1：https://www.bilibili.com/video/BV1u4FYeeEWi/
# Hint2：https://www.bilibili.com/video/BV1vm4y1V7n2/
# Hint3：https://www.bilibili.com/video/BV1qL411J7U5/
# Hint4：https://www.bilibili.com/video/BV1GJ411x7h7/
# 如果你实在需要Hint，可以参考上述URL。
# Flag在环境变量里

import ast
import sys
import importlib

class ImportOnlySandbox:
    def check_code(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            raise ValueError(f"Error")
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.Import, ast.ImportFrom, ast.alias)):
                continue
            return False
        return True


if __name__ == "__main__":
    while True:
        code = input("input your code to be executed: ")
        checker = ImportOnlySandbox()
        try:
            if checker.check_code(code):
                exec(code)
            else:
                print("No")
        except:
            print("Error")