# 极限竞速！ 首尾呼应！
# 希望玩的开心。这题可以随时讨论（包括找出题人）。
# wp会跟着官方wp一起发布哦
# flag在/flag

if __name__ == "__main__":
    blacklist = ['=']
    blacklist.extend(dir('HAVE FUN! I HOPE YOU ENJOY IT!'))
    blacklist.extend(dir(object))
    while True:
        try:
            code = input("input your code to be executed: ")
            if any(char in blacklist for char in code):
                print("No")
            exec(code, {"__builtins__": None, "license": license})
        except:
            print("Error")
