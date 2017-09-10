# sql operation
# -*- coding: UTF-8 -*-
import MySQLdb

config = {
	'host': 'localhost',
	'port': 3306,
	'user': 'root',
	'passwd': 'huochai123',
	'db': 'gsa',
	'charset': 'utf8'
}
conn = MySQLdb.connect(**config)
cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)

def create_tables():
  sqls =  [
          """
            CREATE TABLE IF NOT EXISTS user(
            login  VARCHAR(128) NOT NULL,
            id INT UNSIGNED,
            type CHAR(64),
            name VARCHAR(128),
            company VARCHAR(128),
            location VARCHAR(128),
            public_repos INT UNSIGNED,
            public_gists INT UNSIGNED,
            followers INT UNSIGNED,
            following INT UNSIGNED,
            created_at CHAR(64),
            updated_at CHAR(64),
            spider_updated_at CHAR(64),
            PRIMARY KEY (login)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8; 
          """,
          """
            CREATE TABLE IF NOT EXISTS repo(
            full_name  VARCHAR(128) NOT NULL,
            id INT UNSIGNED,
            owner_login VARCHAR(128),
            name VARCHAR(128),
            private CHAR(10),
            fork CHAR(10),
            language VARCHAR(64),
            forks_count INT UNSIGNED,
            stargazers_count INT UNSIGNED,
            watchers_count INT UNSIGNED,
            size INT UNSIGNED,
            open_issues_count INT UNSIGNED,
            pushed_at CHAR(64),
            created_at CHAR(64),
            updated_at CHAR(64),
            spider_updated_at CHAR(64),
            PRIMARY KEY (full_name)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8; 
          """,
          """
            CREATE TABLE IF NOT EXISTS user_user(
            followed  VARCHAR(128) NOT NULL,
            following VARCHAR(128) NOT NULL,
            PRIMARY KEY (followed,following)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8;
          """,
          """
            CREATE TABLE IF NOT EXISTS user_repo(
            user VARCHAR(128) NOT NULL,
            repo VARCHAR(128) NOT NULL,
            PRIMARY KEY (user,repo)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8;
          """
         ]
  for s in sqls:
    print "EXECUTE CREATE TABLE : \n" + s
    try:
      cursor.execute(s)
      conn.commit()
    except:
      print "CREATE ERROR"
      conn.rollback()

def drop_tables():
  ts = ['user', 'repo', 'user_user', 'user_repo']
  for tb in ts:
    s = "DROP TABLE IF EXISTS %s"%(tb)
    print "EXECUTE DROP : \n" + s
    try:
      cursor.execute(s)
      conn.commit()
    except:
      print "DROP ERROR"
      conn.rollback()

def insert(table_name, item):
  placeholders = ', '.join(['%s']* len(item))
  cols = ', '.join(item.keys())
  s =  "INSERT INTO %s ( %s ) VALUES ( %s )" % (table_name, cols, placeholders)
  #print "EXECUTE INSERT : \n" + s
  try:
    cursor.execute(s, item.values())
    conn.commit()
  except:
    print "INSERT ERROR"
    conn.rollback()

def delete(table_name, key, value):
  s = "DELETE FROM %s WHERE %s = '%s'" % (table_name, key, value)
  #print "EXECUTE DELETE : \n" + s
  try:
    cursor.execute(s)
    conn.commit()
  except:
    print "DELETE ERROR"
    conn.rollback()

def select(table_name, keys):
  cols = ', '.join(keys)
  s = "SELECT DISTINCT %s FROM %s" % (cols, table_name)
  #print "EXECUTE SELECT : \n" + s
  try:
    cursor.execute(s)
    res = cursor.fetchall()
    return res
  except:
    print "SELECT ERROR"
    return None
    
