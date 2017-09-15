import sys
sys.path.append('../')
from data.data.database import sql
from flask import Flask
import flask
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


@app.route('/users/page', defaults={'page': 1})
@app.route('/users/page/<int:page>')
def users_list(page):
    if flask.g.get('users') is None:
        flask.g.users = sql.select('user',['login','followers'])
    per_page = 100
    users = []
    info = dict()
    for i in range((page-1)*per_page, page*per_page):
        if i < len(flask.g.users):
            users.append(flask.g.users[i])
    info['page'] = page
    info['num'] = len(users)
    info['all_user'] = len(flask.g.users)
    info['per_page'] = per_page
    return flask.render_template('user_list.html', info = info, users = users)

@app.route('/repos/page', defaults={'page': 1})
@app.route('/repos/page/<int:page>')
def repos_list(page):
    if flask.g.get('repos') is None:
        flask.g.repos = sql.select('repo',['full_name','stargazers_count','language','size'])
    per_page = 100
    repos = []
    info = dict()
    for i in range((page-1)*per_page, page*per_page):
        if i < len(flask.g.repos):
            repos.append(flask.g.repos[i])
    info['page'] = page
    info['num'] = len(repos)
    info['all_repo'] = len(flask.g.repos)
    info['per_page'] = per_page
    return flask.render_template('repo_list.html', info = info, repos = repos)

if __name__ == '__main__':
    app.run(debug=True)
