#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2019/10/23 15:27
# @Author  : Alex Kwan
# @Email   : gjy-alex@hotmail.com
# @File    : db.py

import sqlite3
import os
import utils.tools

class DataBase (object) :


    def __init__ (self) :
        self.dbAddress = 'database/'
        self.table = 'playlists'
        self.T = utils.tools.Tools()
        self.T.mkdir(self.dbAddress)
        self.T.del_file(self.dbAddress)
        if self.connect() == False:
            self.connStat = False
        else :
            self.connStat = True
            self.chkTable()

    def __del__ (self) :
        if self.connStat == True :
            self.disConn()

    def connect (self) :
        try:
            if not os.path.exists(self.dbAddress) :
                os.makedirs(self.dbAddress)
            self.dbAddress += 'db.sqlite3'
            self.conn = sqlite3.connect(self.dbAddress)
            self.cur = self.conn.cursor()
            return True
        except :
            return False

    def create (self) :
        if self.connStat == False : return False

        sql = 'create table ' + self.table + ' (id integer PRIMARY KEY autoincrement, title text, url text, delay integer, updatetime text)'
        self.cur.execute(sql)

    def query (self, sql) :
        if self.connStat == False : return False

        self.cur.execute(sql)
        values = self.cur.fetchall()

        return values

    def execute (self, sql) :
        try :
            if self.connStat == False : return False
            self.cur.execute(sql)
            return True
        except :
            return False

    def insert (self, data):
        if self.connStat == False : return False

        keyList = []
        valList = []
        for k, v in data.items():
            keyList.append(k)
            valList.append(str(v).replace('"','\"').replace("'","''"))

        sql = "insert into " + self.table + " (`" + '`, `'.join(keyList) + "`) values ('" + "', '".join(valList) + "')"
        self.cur.execute(sql)
        self.conn.commit()

    def edit (self, id, data):
        if self.connStat == False : return False

        param = ''
        for k, v in data.items():
            param = param + ", `%s` = '%s'" %(k, str(v).replace('"','\"').replace("'","''"))

        param = param[1:]

        sql = "update " + self.table + " set %s WHERE id = %s" % (param, id)
        self.cur.execute(sql)
        self.conn.commit()

    def disConn (self) :
        if self.connStat == False : return False

        self.cur.close()
        self.conn.close()

    def chkTable (self) :
        if self.connStat == False : return False

        sql = "SELECT tbl_name FROM sqlite_master WHERE type='table'"
        tableStat = False

        self.cur.execute(sql)
        values = self.cur.fetchall()

        for x in values:
            if self.table in x :
                tableStat = True

        if tableStat == False :
            self.create()

if __name__ == '__main__':
    db = DataBase()
    #print(db.connect())
    #print(db.create())
    #print(db.chkTable())
