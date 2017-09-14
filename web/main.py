import sys
sys.path.append('../')
from data.data.database import sql
from flask import Flask
app = Flask("GSA_web")

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/repos')
def repos():
    res = sql.select('repo',['full_name'])  
    return 'repo num : ' + str(len(res))

@app.route('/users')
def users():
    res = sql.select('user',['login'])
    return 'user num : ' + str(len(res))

if __name__ == '__main__':
    app.run(debug=True)
