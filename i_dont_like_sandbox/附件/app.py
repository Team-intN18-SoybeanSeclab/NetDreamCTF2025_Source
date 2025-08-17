# 上次可恶的嘿课把我沙箱打烂了，你们太坏了。
# 预热题到这里结束，我们正赛再见。玩得开心！
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
