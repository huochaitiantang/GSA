import sql

sql.drop_tables()
sql.create_tables()

item = {
	"public_repos": 4, 
	"name": "Linus Torvalds", 
	"company": "Linux Foundation",
	"updated_at": "2017-04-12T15:12:19Z",
	"created_at": "2011-09-03T15:26:22Z",
	"following": 0,
	"location": "Portland, OR",
	"followers": 53085, 
	"login": "torvalds",
	"type": "User",
	"id": 1024025,
}
sql.insert('user',item)

res = sql.select('user',['login'])
print "Result:",res

#sql.delete('user', 'login', 'torvalds')

uu = {
	'followed': '123',
	'following': '456'
}
ww = {
	'followed': '123',
	'following': '789'
}
vv = {
	'followed': '456',
	'following': '789'
}

sql.insert('user_user',uu)
sql.insert('user_user',ww)
sql.insert('user_user',vv)

res2 = sql.select('user_user',['followed'])
res3 = sql.select('user_user',['following'])
res4 = sql.select('user_user',['followed','following'])

print res2, res3, res4

sql.delete('user_user','followed','123')
sql.delete('user_user','following','789')


