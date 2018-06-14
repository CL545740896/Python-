#-*- coding: utf-8 -*-
""" 
数据库管理类 
"""
import MySQLdb
from DBUtils.PooledDB import PooledDB
#自定义的配置文件，主要包含DB的一些基本配置


#数据库实例化类
class DbManager():

    def __init__(self):
        connKwargs = {'host':'127.0.0.1', 'user':'root', 'passwd':'root', 'db':'db_spyder', 'charset':"utf8"}
        self._pool = PooledDB(MySQLdb, mincached=0, maxcached=10, maxshared=10, maxusage=10000, **connKwargs)

    def getConn(self):
        print 'GET'
        return self._pool.connection()

_dbManager = DbManager()

def getConn():
    """ 获取数据库连接 """
    return _dbManager.getConn()

class Db():

    def inser_data(self,tuple):
        """
        将爬取数据导入数据库
        :param tuple: 抓取下来的数据元组
        :return: 成功1 失败0 异常-1
        """
        try:
            keywords, page, title, href, playtime, subtitle, date_time=tuple
            sql="INSERT INTO t_bilibili(keywords,page,title,href,playnums,subtitle,date_time) VALUES " \
                "('{0}',{1},'{2}','{3}','{4}','{5}','{6}')".format(keywords,page,title,href,playtime,subtitle,date_time)   #字段为字符串类型时,需要加单引号包围数值
            print sql
            conn = getConn()
            cursor = conn.cursor()
            rowcount = cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
            return rowcount
        except Exception as e:
            print e
            return -1








