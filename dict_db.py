"""
数据库功能封装
为服务端提供它所需的数据
"""
import pymysql


class Database:
    def __init__(self):
        # 连接数据库
        self.db = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="123456",
            database='dict',
            charset='utf8')

    def close(self):
        self.db.close()

        # 创建游标

    def cursor(self):
        self.cur = self.db.cursor()

    #　满足服务端注册功能对应的数据需求
    def register(self, name, passwd):
        # 按照姓名查询
        sql = "select name from user where name=%s;"
        self.cur.execute(sql,[name])
        r = self.cur.fetchone() # 得到结果
        if r:
            # 如果查到了而结果 不允许注册
            return False

        # 如果允许择插入用户数据
        sql = "insert into user (name,passwd) values (%s,%s);"
        try:
            self.cur.execute(sql,[name,passwd])
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            return False

    # 处理登录
    def login(self,name,passwd):
        # 按照用户名密码查询
        sql = "select name from user where name=%s and passwd=%s;"
        self.cur.execute(sql, [name,passwd])
        r = self.cur.fetchone()
        if r:
            return True
        else:
            return False

    # 提供单词解释
    def query(self,word):
        sql = "select mean from words where word=%s;"
        self.cur.execute(sql,[word])
        r = self.cur.fetchone() # 考虑查询不到情况
        # r --> (mean,) or None
        if r:
            return r[0] # 返回解释
        else:
            return "Not Found"

    # 插入历史记录
    def insert_history(self,name,word):
        # name time user_id
        # 先查询用户ID
        sql = "select id from user where name=%s;"
        self.cur.execute(sql,[name])
        user_id = self.cur.fetchone()[0]

        # 插入历史记录
        sql = "insert into history (word,user_id) values (%s,%s);"
        try:
            self.cur.execute(sql,[word,user_id])
            self.db.commit()
        except:
            self.db.rollback()

    def history(self,name):
        # 需要 name,word,time
        sql="select name,word,time " \
            "from user left join history " \
            "on user.id=history.user_id " \
            "where name=%s " \
            "order by time desc " \
            "limit 10;"
        self.cur.execute(sql,[name])
        # ((name,word,time),(),())
        return self.cur.fetchall()