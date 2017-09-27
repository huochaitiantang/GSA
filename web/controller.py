import sys
sys.path.append('../')
from data.data.database import sql
import flask
from flask import request
import time
import json

def do_home():
    return flask.render_template('home.html',nav='home')

def do_home_msg():
    info = {}
    info['user'] = sql.get_num('user')
    info['repo'] = sql.get_num('repo')
    info['user_user'] = sql.get_num('user_user')
    info['user_repo'] = sql.get_num('user_repo')
    return json.dumps(info)
    

# show all users
def do_users(page):
    company = request.args.get('company')
    location = request.args.get('location')
    order_type = request.args.get('order_type')
    order = request.args.get('order')
    name = request.args.get('name')
    if company is None:
        company = ''
    if location is None:
        location = ''
    if order_type is None:
        order_type = 'default'
    if order is None:
        order = 'up'
    if name is None:
        name = ''
    users_res = sql.get_users(name,company,location,order_type,order,['login','company','location','public_repos','public_gists','followers'])
    if users_res:
        users_num = len(users_res)
    else:
        users_num = 0
    per_page = 100
    x = 0
    if users_num % per_page == 0:
        x = 1
    if page < 1:
        return flask.redirect('/users/page/1?order_type=%s&order=%s&company=%s&location=%s&name=%s'%(order_type,order,company,location,name))
    lst_page = int(users_num/per_page) + 1 - x
    if lst_page > 0 and page > lst_page:
        return flask.redirect('/users/page/%d?order_type=%s&order=%s&company=%s&location=%s&name=%s'%(lst_page,order_type,order,company,location,name))
    users = []
    for i in range((page-1)*per_page, page*per_page):
        if users_res and i < users_num and i >=0:
            users.append(users_res[i])
    info = dict()
    info['page'] = page
    info['lst_page'] = lst_page
    info['num'] = len(users)
    info['all_user'] = users_num
    info['per_page'] = per_page
    info['all_order_type'] = ['followers','public_repos','public_gists']
    info['company'] = company
    info['location'] = location
    info['order_type'] = order_type
    info['order'] = order
    info['name'] = name
    #print users
    return flask.render_template('user_list.html', info = info, users = users, nav='users')


# show all repos
def do_repos(page):
    lan = request.args.get('language')
    order_type = request.args.get('order_type')
    order = request.args.get('order')
    name = request.args.get('name')
    if lan is None:
        lan = 'default'
    if order_type is None:
        order_type = 'default'
    if order is None:
        order = 'up'
    if name is None:
        name = ''
    repos_res = sql.get_repos(name,lan,order_type,order,['full_name','stargazers_count','language','size'])
    if repos_res:
        repos_num = len(repos_res)
    else:
        repos_num = 0
    per_page = 100
    x = 0
    if repos_num % per_page == 0:
        x = 1
    lst_page = int(repos_num/per_page) + 1 - x
    if page < 1:
        return flask.redirect('/repos/page/1?order_type=%s&order=%s&language=%s&name=%s'%(order_type, order, lan, name))
    if lst_page > 0 and page > lst_page:
        return flask.redirect('/repos/page/%d?order_type=%s&order=%s&language=%s&name=%s'%(lst_page, order_type, order, lan,name))
    repos_lan_res = sql.get_repo_language()
    repos = []
    repos_lan = []
    for i in range((page-1)*per_page, page*per_page):
        if repos_res and i < repos_num and i >= 0 :
            repos.append(repos_res[i])
    for la in repos_lan_res:
        if la['language'] is None:
            repos_lan.append('None')
        else:
            repos_lan.append(la['language'])
    info = dict()
    info['page'] = page
    info['lst_page'] = lst_page
    info['num'] = len(repos)
    info['all_repo'] = repos_num
    info['per_page'] = per_page
    info['all_language'] = repos_lan
    info['all_order_type'] = ['stargazers_count','size']
    info['language'] = lan
    info['order_type'] = order_type
    info['order'] = order
    info['name'] = name
    return flask.render_template('repo_list.html', info = info, repos = repos, nav='repos')


def do_repos_statistics():
    stype = request.args.get('type')
    star_gap = request.args.get('star_gap')
    size_gap = request.args.get('size_gap')
    star_gaps = [2,3,4,5,10]
    size_gaps = [2,3,4,5,10]
    #star_gaps = sql.get_gaps('repo','stargazers_count')
    #size_gaps = sql.get_gaps('repo','size')
    if star_gap:
        star_gap = int(star_gap)
    if star_gap not in star_gaps:
            star_gap = star_gaps[0]
    if size_gap:
        size_gap = int(size_gap)
    if size_gap not in size_gaps:
            size_gap = size_gaps[0]
    if stype is None:
        stype = 'language'
    info = dict()
    info['type'] = stype
    info['star_gap'] = star_gap
    info['size_gap'] = size_gap
    info['star_gaps'] = star_gaps
    info['size_gaps'] = size_gaps
    return flask.render_template('repo_statistics.html',info=info,nav='repos-statistics')

def do_repos_statistics_msg():
    stype = request.args.get('type')
    star_gap = request.args.get('star_gap')
    size_gap = request.args.get('size_gap')
    star_gaps = [2,3,4,5,10]
    size_gaps = [2,3,4,5,10]
    #star_gaps = sql.get_gaps('repo','stargazers_count')
    #size_gaps = sql.get_gaps('repo','size')
    if star_gap:
        star_gap = int(star_gap)
    if star_gap not in star_gaps:
            star_gap = star_gaps[0]
    if size_gap:
        size_gap = int(size_gap)
    if size_gap not in size_gaps:
            size_gap = size_gaps[0]
    if stype is None:
        stype = 'language'
    ans = {
        'type':'Response',
        'timestamp': int(time.time() * 1000)
    }
    #equalgap = True
    equalgap = False
    if stype == 'language':
        ans['key_val'] = sql.get_num_by_group('repo','language')
    elif stype == 'stargazers_count':
        ans['key_val'] = sql.get_num_by_gap('repo',stype,star_gap,equalgap)
    elif stype == 'size':
        ans['key_val'] = sql.get_num_by_gap('repo',stype,size_gap,equalgap)
    else:
        print "ERROR"
    return json.dumps(ans)

def do_users_statistics():
    stype = request.args.get('type')
    gap = dict()
    gaps = dict()
    keys = ['followers_gap','public_repos_gap','public_gists_gap']
    for k in keys:
        gap[k] = request.args.get(k)
        gaps[k] = [2,3,4,5,10]
        if gap[k]:
            gap[k] = int(gap[k])
        if gap[k] not in gaps[k]:
            gap[k] = gaps[k][0]
    #print gap
    if stype is None:
        stype = 'followers'
    info = dict()
    info['type'] = stype
    for k in keys:
        info[k] = gap[k]
        info[k+'s'] = gaps[k]
    #print info
    return flask.render_template('user_statistics.html',info=info,nav='users-statistics')

def do_users_statistics_msg():
    stype = request.args.get('type')
    gap = dict()
    gaps = dict()
    keys = ['followers_gap','public_repos_gap','public_gists_gap']
    for k in keys:
        gap[k] = request.args.get(k)
        gaps[k] = [2,3,4,5,10]
        if gap[k]:
            gap[k] = int(gap[k])
        if gap[k] not in gaps[k]:
            gap[k] = gaps[k][0]
    if stype is None:
        stype = 'followers'
    ans = {
        'type':'Response',
        'timestamp': int(time.time() * 1000)
    }
    #equalgap = True
    equalgap = False
    for k in keys:
        if stype+'_gap' == k:
            ans['key_val'] = sql.get_num_by_gap('user',stype,gap[k],equalgap)
    return json.dumps(ans)
