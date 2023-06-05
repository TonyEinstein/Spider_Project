#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :pymysql_insertdata.py
# @Time      :2023/1/7 10:09
# @Author    : https://github.com/chenruhai?tab=repositories
import time
import pandas as pd
import pymysql

class Pmysql:
    def __init__(self):
        # 打开数据库连接
        self.conn = pymysql.connect(host="localhost", user="root", password="11080226", port=3306)
        # 使用cursor()方法获取操作游标
        self.cursor = self.conn.cursor()


    def delete_table(self,database_name="test",table_name="user"):
        sql = "DROP TABLE IF EXISTS {};".format(table_name)
        try:
            self.conn.ping()
            # 指定使用数据库
            self.cursor.execute('use {};'.format(database_name))
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            print("删除表任务 提交成功，提交时间：{}".format(time.strftime('%Y-%m-%d %H:%M:%S')))
        except Exception as e:
            # 如果发生错误则回滚
            self.conn.rollback()
            print("删除表任务 提交失败：{},报错内容：".format(time.strftime('%Y-%m-%d %H:%M:%S')), e)

    def delete_database(self,database_name="test"):
        sql = "DROP DATABASE IF EXISTS {};".format(database_name)
        try:
            self.conn.ping()
            # 指定使用数据库
            self.cursor.execute('use {};'.format(database_name))
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            print("删除数据库任务 提交成功，提交时间：{}".format(time.strftime('%Y-%m-%d %H:%M:%S')))
        except Exception as e:
            # 如果发生错误则回滚
            self.conn.rollback()
            print("删除数据库任务 提交失败：{},报错内容：".format(time.strftime('%Y-%m-%d %H:%M:%S')), e)

    def creat_database(self,database_names="test"):
        sql = "create database if not exists {} default charset utf8 default collate utf8_general_ci;".format(database_names)
        try:
            self.conn.ping()
            # 执行sql语句
            self.cursor.execute(sql)
            # 指定使用数据库
            self.cursor.execute('use {};'.format(database_names))
            # 提交到数据库执行
            self.conn.commit()
            print("创建数据库任务 提交成功，提交时间：{}".format(time.strftime('%Y-%m-%d %H:%M:%S')))
        except Exception as e:
            # 如果发生错误则回滚
            self.conn.rollback()
            print("创建数据库任务 提交失败：{},报错内容：".format(time.strftime('%Y-%m-%d %H:%M:%S')), e)

    def create_table(self,database_names="test",
                     sql = "create table IF NOT EXISTS user( \
                    id integer not null auto_increment primary key, \
                    mail varchar(255) not null, \
                    name varchar(255) not null, \
                    number varchar(255), \
                    created timestamp not null default '0000-00-00 00:00:00', \
                    updated timestamp not null default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP \
                  ) DEFAULT CHARSET=utf8mb4;"):
        try:
            self.conn.ping()
            # 指定使用数据库
            self.cursor.execute('use {};'.format(database_names))
            # 执行 sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            print("创建表任务提交成功，提交时间：{}".format(time.strftime('%Y-%m-%d %H:%M:%S')))
        except Exception as e:
            # 如果发生错误则回滚
            self.conn.rollback()
            print("创建表任务 提交失败：{},报错内容：".format(time.strftime('%Y-%m-%d %H:%M:%S')), e)

    def insert_data(self,data_list,database_names="test",sql = "INSERT INTO user(mail,name,number)VALUES ({}, {},{});".format('%s', '%s', '%s')):
        """
        插入多个数据
        :param cursor:
        :param conn:
        :return:
        """
        # SQL 插入语句
        try:
            self.conn.ping()
            # 指定使用数据库
            self.cursor.execute('use {};'.format(database_names))
            # 执行sql语句
            self.cursor.executemany(sql,data_list)
            # 提交到数据库执行
            self.conn.commit()
            print("插入多行数据任务 提交成功，提交时间：{}".format(time.strftime('%Y-%m-%d %H:%M:%S')))
        except Exception as e:
            # 如果发生错误则回滚
            self.conn.rollback()
            print("插入多行数据任务 提交失败：{},报错内容：".format(time.strftime('%Y-%m-%d %H:%M:%S')), e)

    def insert_one(self,database_names="test",
                   sql = "INSERT INTO user(mail,name,number)VALUES ('123456@qq.com', '张三','12345678999');"):
        """
        插入一个数据
        :param data:
        :param cursor:
        :param conn:
        :return:
        """
        # SQL 插入语句
        try:
            self.conn.ping()
            # 指定使用数据库
            self.cursor.execute('use {};'.format(database_names))
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            print("插入单行数据任务 提交成功，提交时间：{}".format(time.strftime('%Y-%m-%d %H:%M:%S')))
        except Exception as e:
            # 如果发生错误则回滚
            self.conn.rollback()
            print("插入单行数据任务 提交失败：{},报错内容：".format(time.strftime('%Y-%m-%d %H:%M:%S')), e)

    def close(self):
        # 关闭游标
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()

    def close_cursor(self):
        # 关闭游标
        self.cursor.close()

    def close_conn(self):
        # 关闭数据库连接
        self.conn.close()


if __name__ == '__main__':
    # df = pd.read_excel("to_addrs.xlsx",sheet_name="2023-01-07",dtype={'number' : str})
    # df = df.where(df.notnull(), None)
    # df_list = df.values.tolist()
    p = Pmysql()
    p.creat_database(database_names="test")
    p.create_table(database_names="test")

    # p.insert_one(database_names="test")
    # data = [['1457779389@qq.com', '许玉雯', ''],['1457779389@qq.com', '许玉雯', '1235'],['1457779389@qq.com', '许玉雯222', '']]
    # p.insert_data(data_list=data,database_names="test")
    p.delete_table(database_name="test",table_name="user")
    p.delete_database(database_name="test")
    p.close()


