# sql operation
# -*- coding: UTF-8 -*-
import MySQLdb
import re

def get_conn():
    config = {
	'host': 'localhost',
	'port': 3306,
	'user': 'root',
	'passwd': 'huochai123',
	'db': 'gsa',
	'charset': 'utf8'
    }
    conn = MySQLdb.connect(**config)
    return conn

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
  conn = get_conn()
  cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
  for s in sqls:
    print "EXECUTE CREATE TABLE : \n" + s
    try:
      cursor.execute(s)
      conn.commit()
    except:
      print "CREATE ERROR"
      conn.rollback()
  cursor.close()
  conn.close()

def drop_tables():
  ts = ['user', 'repo', 'user_user', 'user_repo']
  conn = get_conn()
  cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
  for tb in ts:
    s = "DROP TABLE IF EXISTS %s"%(tb)
    print "EXECUTE DROP : \n" + s
    try:
      cursor.execute(s)
      conn.commit()
    except:
      print "DROP ERROR"
      conn.rollback()
  cursor.close()
  conn.close()

def insert(table_name, item):
  placeholders = ', '.join(['%s']* len(item))
  cols = ', '.join(item.keys())
  s =  "INSERT INTO %s ( %s ) VALUES ( %s )" % (table_name, cols, placeholders)
  #print "EXECUTE INSERT : \n" + s
  conn = get_conn()
  cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
  try:
    cursor.execute(s, item.values())
    conn.commit()
  except:
    print "INSERT ERROR"
    conn.rollback()
  cursor.close()
  conn.close()

def delete(table_name, key, value):
  s = "DELETE FROM %s WHERE %s = '%s'" % (table_name, key, value)
  #print "EXECUTE DELETE : \n" + s
  conn = get_conn()
  cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
  try:
    cursor.execute(s)
    conn.commit()
  except:
    print "DELETE ERROR"
    conn.rollback()
  cursor.close()
  conn.close()

def select(table_name, keys):
  cols = ', '.join(keys)
  s = "SELECT DISTINCT %s FROM %s" % (cols, table_name)
  conn = get_conn()
  cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
  #print "EXECUTE SELECT : \n" + s
  try:
    cursor.execute(s)
    res = cursor.fetchall()
  except:
    print "SELECT ERROR"
    res = None
  cursor.close()
  conn.close()
  return res
  
def get_repo_language():
  s = "SELECT DISTINCT language FROM repo ORDER BY language"
  conn = get_conn()  
  cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
  try:
    cursor.execute(s)
    res = cursor.fetchall()
  except:
    print "SELECT ERROR"
    res = None
  cursor.close()
  conn.close()
  return res

def get_repos(name, language, order_type, order, keys):
  cols = ','.join(keys)
  s = "SELECT %s FROM repo"%(cols)
  params = []
  if language and language != 'default':
    if language != 'None':
      s += " WHERE language = '%s'"%(language)
    else:
      s += " WHERE language is NULL"
  if name and len(name) > 0:
    if language and language != 'default':
      s += " AND"
    else:
      s += " WHERE"
    name = "%" + re.sub("/W","%",name) + "%"
    s += " full_name LIKE %s"
    params.append(name)
  if order_type and order_type != 'default':
    s += " ORDER BY %s"%(order_type)
    if order == 'down':
      s += " DESC"
  print s
  conn = get_conn()  
  cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
  try:
    cursor.execute(s,params)
    res = cursor.fetchall()
  except:
    print "SELECT ERROR"
    res = None
  cursor.close()
  conn.close()
  return res

def get_users(name, company, location, order_type, order, keys):
  cols = ','.join(keys)
  params = []
  s = "SELECT %s FROM user"%(cols)
  if name and len(name) > 0:
    name = "%" + re.sub("/W","%",name) + "%"
    s += " WHERE login LIKE %s"
    params.append(name)
  if company and len(company) > 0:
    company = "%" + re.sub("/W","%",company) + "%"
    if name and len(name) > 0:
      s += " AND"
    else:
      s += " WHERE"
    s += " company LIKE %s"
    params.append(company)
  if location and len(location) > 0:
    location = "%" + re.sub("/W","%",location) + "%"
    if (name and len(name)) or (company and len(company) > 0):
      s += " AND"
    else:
      s += " WHERE"
    s += " location LIKE %s"
    params.append(location)
  if order_type and order_type != 'default':
    s += " ORDER BY %s"%(order_type)
    if order == 'down':
      s += " DESC"
  print s,params
  conn = get_conn()  
  cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
  try:
    cursor.execute(s,params)
    res = cursor.fetchall()
  except:
    print "SELECT ERROR"
    res = None
  cursor.close()
  conn.close()
  return res

def get_gaps(table_name, key):
  ind = 'MAX(%s)'%(key)
  s = "SELECT %s FROM %s"%(ind,table_name)
  conn = get_conn()  
  cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
  try:
    cursor.execute(s)
    max_num = int(cursor.fetchall()[0][ind])
  except:
    print "SELECT ERROR"
    max_num = 0
  max_gap = max_num/20
  min_gap = (max_num/300/100)*100
  gap_gap = ((max_gap-min_gap)/20)/100*100
  print max_num,min_gap,max_gap,gap_gap
  ans = []
  ans.append(min_gap)
  for i in range(1,20):
    x = ans[i-1] + gap_gap
    ans.append(x)
  cursor.close()
  conn.close()
  return ans 

def get_num_by_group(table_name, key):
  conn = get_conn()  
  cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
  s = "SELECT DISTINCT %s FROM %s ORDER BY %s"%(key,table_name,key)
  try:
    cursor.execute(s)
    res = cursor.fetchall()
  except:
    print "SELECT ERROR"
    res = ()
  ans = []
  for r in res:
    cur = dict()
    if r[key] is None:
      cur['key'] = 'None'
      s = "SELECT COUNT(*) FROM %s WHERE %s is NULL"%(table_name,key)
    else: 
      cur['key'] = r[key]
      s = "SELECT COUNT(*) FROM %s WHERE %s = '%s'"%(table_name,key,r[key])
    try:
      cursor.execute(s)
      cur['val'] = int(cursor.fetchall()[0]['COUNT(*)'])
    except:
      cur['val'] = 0
    ans.append(cur)
  cursor.close()
  conn.close()
  return sorted(ans, key = lambda x:x['val'], reverse=True)

def get_num_by_gap(table_name,key,gap):
  conn = get_conn()  
  cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
  ind = 'MAX(%s)'%(key)
  s = "SELECT %s FROM %s"%(ind,table_name)
  try:
    cursor.execute(s)
    max_num = int(cursor.fetchall()[0][ind])
  except:
    print "SELECT ERROR"
    max_num = 0
  ans = []
  pre = 0
  k = gap
  while True:
    cur = dict()    
    cur['key'] = str(pre)+'-'+str(k)
    s = "SELECT COUNT(*) FROM %s WHERE %s >= %d and %s < %d"%(table_name,key,pre,key,k)
    print s
    try:
      cursor.execute(s)
      cur['val'] = int(cursor.fetchall()[0]['COUNT(*)'])
    except:
      print "SELECT ERROR"
      cur['val'] = 0
    ans.append(cur)
    if k > max_num:
      break
    pre = k
    k = k * gap
  cursor.close()
  conn.close()
  return ans






