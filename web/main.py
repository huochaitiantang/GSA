import flask
import controller
app = flask.Flask("GSA_web")

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/users/page', defaults={'page': 1})
@app.route('/users/page/<int:page>')
def users(page):
    return controller.do_users(page)

@app.route('/repos/page', defaults={'page': 1})
@app.route('/repos/page/<int:page>')
def repos_list(page):
    return controller.do_repos(page)

@app.route('/repos/statistics/')
def repos_statistics():
    return controller.do_repos_statistics()

@app.route('/repos/statistics/msg')
def repos_statistics_msg():
    return controller.do_repos_statistics_msg()

@app.route('/users/statistics/')
def users_statistics():
    return controller.do_users_statistics()

@app.route('/users/statistics/msg')
def users_statistics_msg():
    return controller.do_users_statistics_msg()

if __name__ == '__main__':
    app.run(debug=True)
