import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretsecret'


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    user = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username, password)
        return redirect(url_for('home', user_id=user['user_id']))
    return render_template('login.html')

@app.route('/edit/<post_id>', methods=('GET', 'POST'))
def edit(post_id):
    post = get_post(post_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE post_id = ?',
                         (title, content, post_id))
            conn.commit()
            conn.close()
            return redirect(url_for('home', user_id=post['user_id']))

    return render_template('edit.html', post=post)

@app.route('/create/<user_id>', methods=['GET', 'POST'])
def create(user_id):
    if request.method == 'POST':
        text = request.form['writing']
        title = request.form['title']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)",
             (user_id,title, text)
                )
        conn.commit()
        conn.close()
        return redirect(url_for('home', user_id=user_id))
    return render_template('create.html', user_id=user_id)

@app.route('/home/<user_id>')
def home(user_id):
    user = get_user_from_id(user_id)
    user_posts = get_user_posts(user_id)
    return render_template('home.html', user=user, user_posts=user_posts)

@app.route('/delete/<post_id>', methods=('POST',))
def delete(post_id):
    post = get_post(post_id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE post_id = ?', (post_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('home', user_id=post['user_id']))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        checkpassword = request.form['checkpassword']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
             (username, password)
                )
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('signin.html')

def get_user(username, password):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                        (username, password,)).fetchone()
    conn.close()
    if user is None:
        abort(404)
    return user

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE post_id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


def get_user_from_id(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE user_id = ?',
                        (user_id,)).fetchone()
    conn.close()
    if user is None:
        abort(404)
    return user


def get_user_posts(user_id):
    conn = get_db_connection()
    userposts = conn.execute('SELECT * FROM posts WHERE user_id = ?',
                        (user_id,)).fetchall()
    conn.close()
    if userposts is None:
        abort(404)
    return userposts

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == "__main__":
  app.run(debug=True)



