"""
解决两个界面相互跳转的问题
"""

# 二级界面
def second():
    # 二级界面
    while True:
        print("""
        ==============  Query  =============
          1. 查单词    2. 历史记录    3. 注销
        ====================================
        """)
        cmd = input("命令:")
        if cmd == '1':
            pass
        elif cmd == '2':
            pass
        elif cmd == '3':
            break
        else:
            print("请输入正确指令")

# 一级界面
while True:
    print("""
    =========== Welcome ===========
     1. 注册    2. 登录    3. 退出
    ===============================
    """)
    cmd = input("命令:")
    if cmd == '1':
        pass
    elif cmd == '2':
        second()
    elif cmd == '3':
        break
    else:
        print("请输入正确指令")


