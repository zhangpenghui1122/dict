"""


将文本 dict.txt的单词插入到该数据表中

提示: 读取文件
      单词和解释提取出来
      插入到数据表中
"""

import pymysql
import re

# 连接数据库 (连接本机可以不写host和port)
db = pymysql.connect(host = "localhost",
                     port = 3306,
                     user = "root",
                     password = "123456",
                     database = "dict",
                     charset = "utf8"
)

# 创建游标 (执行sql语句获取执行结果的对象)
cur = db.cursor()

# 打开文件
f = open('dict.txt')

# args_list--> [(word,mean),(),()]
args_list = []
# 逐行遍历,每行一个单词
for line in f:
    # 提取一行中的单词和解释
    # t->[("a","indef art one")]
    t = re.findall(r"(\w+)\s+(.*)",line)
    args_list.extend(t) # 合并t列表内容到args

# 插入数据表中
sql = "insert into words (word,mean) " \
      "values (%s,%s);"
try:
    cur.executemany(sql,args_list)
    db.commit()
except:
    db.rollback()

# 关闭游标和数据库连接
f.close()
cur.close()
db.close()
