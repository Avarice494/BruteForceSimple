from flask import Flask, request, render_template, make_response, url_for, redirect, session
from jinja2 import Template
from hashlib import md5
from datetime import timedelta



app = Flask(__name__, static_folder='./static')
app.config['SECRET_KEY'] = 'XXXXX'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

user = 'admin'
passwd = '101101'


def getmd5hash(values):
    return md5(values.encode()).hexdigest()

@app.route("/")
def index():
    name = request.args.get('name', 'quest')
    t = Template('Hello '+name)
    return t.render()

@app.route("/login", methods = ['GET', 'POST'])
def login():
    a =  request.form.get('user')
    b = request.form.get('pass')
    if request.method == 'POST':
        if request.form.get('user') == user and request.form.get('pass') == passwd:
            resp = make_response(redirect(url_for('main')))
            resp.set_cookie('user', user, )
            resp.set_cookie('pass', getmd5hash(passwd), )
            return resp
        else:
            if 'errtime' not in session:
                session['errtime'] = 1
            else:
                session['errtime'] = session['errtime'] + 1

            return '登录错误，请返回'+f"{a}:{b}"

    else:
        if 'errtime' in session and session['errtime'] > 2: return "登录次数过多，请稍后再试"
        print('this is get')
        return render_template('login.html')

@app.route("/main")
def main():
    user = request.cookies.get('user')
    passwd = request.cookies.get('pass')
    if user and passwd:
        return render_template('main.html', user=user)

if __name__ == '__main__':
    app.run()