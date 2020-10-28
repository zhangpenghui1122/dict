"""
dict 客户端
* 收集请求
* 发送请求
* 等待结果
* 结果的展示
"""

from socket import *
import sys

ADDR = ('127.0.0.1', 8800)


# =================二级界面功能===========

def do_query(sockfd,name):
    while True:
        word = input("单词:")
        if word == "##":
            break
        # 发送请求
        msg = "Q %s %s"%(name,word)
        sockfd.send(msg.encode())
        # 得到结果
        result = sockfd.recv(4096)
        print(result.decode())

def do_hist(sockfd,name):
    # 发送请求
    msg = "H "+name
    sockfd.send(msg.encode())
    # 无法确定接受次数 不确定这个用户有多少历史记录
    while True:
        # 每次接受一个历史记录
        data = sockfd.recv(1024).decode()
        if data=='##':
            break
        print(data)


# 二级界面
def second(sockfd,name):
    # 二级界面
    while True:
        print("""
        ==============  Query  =============
          1. 查单词   2. 历史记录   3. 注销
        =======================用户:%s=====
        """%name)
        cmd = input("命令:")
        if cmd == '1':
            do_query(sockfd,name)
        elif cmd == '2':
            do_hist(sockfd,name)
        elif cmd == '3':
            break
        else:
            print("请输入正确指令")


# ============== 一级界面功能函数 ==============

def do_register(sockfd):
    while True:
        name = input("Name:")
        passwd = input("Password:")
        if ' ' in passwd or ' ' in name:
            print("用户名或密码不允许空格")
            continue
        passwd_ = input("Again:")
        if passwd != passwd_:
            print("两次密码不一致")
            continue

        # 发送请求
        msg = "R %s %s" % (name, passwd)
        sockfd.send(msg.encode())
        # 等待结果
        result = sockfd.recv(128).decode()
        if result == 'OK':
            print("注册成功")
        else:
            print("注册失败")
        return


def do_login(sockfd):
    name = input("Name:")
    passwd = input("Password:")
    # 发送请求
    msg = "L %s %s" % (name, passwd)
    sockfd.send(msg.encode())
    # 等待结果
    result = sockfd.recv(128).decode()
    if result == 'OK':
        print("登录成功")
        second(sockfd,name)  # 调用二级界面
    else:
        print("登录失败")


# 启动客户端函数
def main():
    sockfd = socket()
    sockfd.connect(ADDR)  # 连接服务端

    # 进入一级界面
    while True:
        print("""
        =========== Welcome ===========
         1. 注册    2. 登录    3. 退出
        ===============================
        """)
        cmd = input("命令:")
        if cmd == '1':
            do_register(sockfd)
        elif cmd == '2':
            do_login(sockfd)
        elif cmd == '3':
            sockfd.send(b"E")
            sys.exit("谢谢使用")
        else:
            print("请输入正确指令")


if __name__ == '__main__':
    main()
