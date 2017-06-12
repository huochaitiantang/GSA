# sql operation
# -*- coding: UTF-8 -*-
import MySQLdb
db = MySQLdb.connect("localhost","root","huochai123","gsa" )
cursor = db.cursor()

def create_tables():
  sqls =  [
          """
            CREATE TABLE IF NOT EXISTS user(
            login  VARCHAR(128) NOT NULL,
            id INT UNSIGNED,
            url VARCHAR(256),
            html_url VARCHAR(256),
            followers_url VARCHAR(256),
            following_url VARCHAR(256),
            starred_url VARCHAR(256),
            repos_url VARCHAR(256),
            type CHAR(64),
            site_admin CHAR(10),
            name VARCHAR(128),
            company VARCHAR(128),
            location VARCHAR(128),
            hireable CHAR(10),
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
            url VARCHAR(256),
            html_url VARCHAR(256),
            stargazers_url VARCHAR(256),
            language VARCHAR(64),
            forks_count INT UNSIGNED,
            stargazers_count INT UNSIGNED,
            watchers_count INT UNSIGNED,
            size INT UNSIGNED,
            open_issues_count INT UNSIGNED,
            push_at CHAR(64),
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
    print "EXECUTE CREATE TABLE : \n"+s
    cursor.execute(s)

def insert(table_name,item):
  s = """
	INSERT
