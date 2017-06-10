# sql operation
# -*- coding: UTF-8 -*-
import MySQLdb
db = MySQLdb.connect("localhost","root","huochai123","gsa" )
cursor = db.cursor()

def create_tables():
  sqls = []
  sqls[0] = """
            create table if not exists user(
            login  ,
            `runoob_id` INT UNSIGNED AUTO_INCREMENT,
   `runoob_title` VARCHAR(100) NOT NULL,
   `runoob_author` VARCHAR(40) NOT NULL,
   `submission_date` DATE,
   PRIMARY KEY ( `runoob_id` )
            )ENGINE=InnoDB DEFAULT CHARSET=utf8; """

  cursor.execute(sql)
