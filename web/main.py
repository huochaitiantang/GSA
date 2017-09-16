import sys
sys.path.append('../')
from data.data.database import sql
from flask import Flask,request
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
    lan = request.args.get('language')
    order_type = request.args.get('order_type')
    order = request.args.get('order')
    if lan is None:
        lan = 'default'
    if order_type is None:
        order_type = 'default'
    if order is None:
        order = 'up'
    repos_res = sql.get_repos(lan,order_type,order,['full_name','stargazers_count','language','size'])
    repos_num = len(repos_res)
    per_page = 100
    x = 0
    if repos_num % per_page == 0:
        x = 1
    lst_page = int(repos_num/per_page) + 1 - x
    if page > lst_page:
        return flask.redirect('/repos/page/%d?order_type=%s&order=%s&language=%s'%(lst_page, order_type, order, lan))
    
    repos_lan_res = sql.get_repo_language()
    repos = []
    repos_lan = []
    for i in range((page-1)*per_page, page*per_page):
        if repos_res and i < len(repos_res):
            repos.append(repos_res[i])
    for la in repos_lan_res:
        repos_lan.append(la['language'])

    info = dict()
    info['page'] = page
    info['lst_page'] = lst_page
    info['num'] = len(repos)
    info['all_repo'] = len(repos_res)
    info['per_page'] = per_page
    info['all_language'] = repos_lan
    info['all_order_type'] = ['stargazers_count','size']
    info['language'] = lan
    info['order_type'] = order_type
    info['order'] = order

    return flask.render_template('repo_list.html', info = info, repos = repos)

if __name__ == '__main__':
    app.run(debug=True)
