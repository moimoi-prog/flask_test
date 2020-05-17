# all the imports
import dao
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash

# configuration
DATABASE = 'mysql+pymysql://root:@127.0.0.1/example_db'
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


# 画面表示用メソッド

@app.route('/')
def show_entries():
    task_dao = dao.Dao()
    list = task_dao.get()
    return render_template('show_entries.html', entries=list)


# ログイン用メソッド

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('ログインしています')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


# ログアウト用メソッド

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('ログアウトしています')
    return redirect(url_for('show_entries'))


# 作業登録用メソッド

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    error = None
    if request.method == 'POST':
        if request.form['name'] is None:
            error = '作業名称を入力してください'
        else:
            task_dao = dao.Dao()
            task_dao.add(request.form["name"])
            list = task_dao.get()
            return render_template('show_entries.html', entries=list)
    return render_template('login.html', error=error)


# 作業削除用メソッド

@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete(task_id):
    error = None
    if request.method == 'POST':
        task_dao = dao.Dao()
        task_dao.delete(task_id)
        list = task_dao.get()
        return render_template('show_entries.html', entries=list)
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run()
