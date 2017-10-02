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

print "Init Done."

