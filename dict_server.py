"""
dict 服务端
* 接受请求
* 逻辑处理
* 向客户端发送数据
"""
from socket import *
from multiprocessing import Process
from signal import *
import sys
from dict_db import *
import time

# 服务端地址
HOST = '0.0.0.0'
PORT = 8800
ADDR = (HOST,PORT)

# 建立数据库连接
db = Database()

# 处理注册
def do_register(connfd,name,passwd):
    if db.register(name,passwd):
        connfd.send(b'OK')
    else:
        connfd.send(b'FAIL')

# 处理登录
def do_login(connfd,name,passwd):
    if db.login(name,passwd):
        connfd.send(b'OK')
    else:
        connfd.send(b'FAIL')

# 处理查单词
def do_query(connfd,name,word):
    # 数据模块查询单词,返回解释
    mean = db.query(word)
    # 发送给客户端
    data = "%s : %s"%(word,mean)
    connfd.send(data.encode())
    # 插入历史记录
    db.insert_history(name,word)

# 历史记录
def do_hist(connfd,name):
    # result -> ((name,word,time),(),())
    result = db.history(name)
    for row in result:
        # row --> (name,word,time)
        msg = "%s    %s    %s"%row
        connfd.send(msg.encode())
        time.sleep(0.1) # 防止粘包
    connfd.send(b"##")

# 客户端处理函数　（进程函数）
def handle(connfd):
    db.cursor() #　为每个进程创建自己的游标
    # 总分的处理模式
    while True:
        # 接收请求
        data = connfd.recv(1024).decode()
        # 解析请求
        tmp = data.split(' ')
        # 根据请求类型分情况讨论
        if not data or data=='E':
            connfd.close()
            db.cur.close() # 关闭游标
            return
        elif tmp[0] == 'R':
            # tmp--> [R,name,passwd]
            do_register(connfd,tmp[1],tmp[2])
        elif tmp[0] == 'L':
            # tmp--> [L,name,passwd]
            do_login(connfd,tmp[1],tmp[2])
        elif tmp[0] == 'Q':
            # tmp--> [Q,name,word]
            do_query(connfd,tmp[1],tmp[2])
        elif tmp[0] == 'H':
            # tmp--> [H,name]
            do_hist(connfd,tmp[1])

# 搭建服务端 多进程网络并发结构
def main():
    # 创建tcp 套接字
    sockfd = socket()
    sockfd.bind(ADDR)

    sockfd.listen(5)
    print("等待客户端连接....")

    # 处理僵尸进程
    signal(SIGCHLD,SIG_IGN)

    # 循环处理客户端连接
    while True:
        try:
            connfd,addr = sockfd.accept()
            print("Connect from",addr)
        except KeyboardInterrupt:
            sockfd.close()
            db.close() # 关闭数据库
            sys.exit()

        # 为连接的客户端创建子进程处理其请求
        p = Process(target=handle,args=(connfd,))
        p.daemon = True
        p.start()

if __name__ == '__main__':
    main()
