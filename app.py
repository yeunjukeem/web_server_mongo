# app.py_web_server_mongo

from flask import Flask, render_template, request, redirect, session,jsonify
from data import Articles
from models import MyMongo
from config import MONGODB_URL
from functools import wraps
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "a"

mymongo = MyMongo(MONGODB_URL , 'os')

def is_logged_in(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'is_logged' in session:
            return func(*args, **kwargs)
        else:
            return redirect('/login')
    return wrap

def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['username'] == "admin":
            return f(*args, **kwargs)
        else:
            return redirect('/login')
    return wrap

@app.route('/admin', methods=['GET', 'POST'])
@is_logged_in 
@is_admin
def admin():
    return render_template('admin.html')

@app.route('/', methods=['GET'])
def index():
    article = Articles()
    return render_template('index.html', contents=article)


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        user = mymongo.find_user(email)
        if user:
            return redirect('/register')
        else:
            if username == "admin":
                return redirect('/register')
            else:                    
                mymongo.user_insert(username , email , phone , password)
                print(username , email , phone , password)
                return redirect('/login')
            
    elif request.method == 'GET':
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        result = mymongo.verify_password(password, email)
        user = mymongo.find_user(email)
        if result == "1":
            session['is_logged'] = True
            session['username'] = user['username']
            return render_template('index.html', msg=user)
        elif result == "2":
            return render_template('login.html', msg="Wrong")
        elif result == "3":
            return render_template('register.html', msg="NONE")

        return result
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
   
@app.route('/list', methods=['GET','POST'])
def list():
    data = mymongo.find_data()
    return render_template('list.html', data=data)
   
@app.route('/create_at', methods=['GET','POST'])
@is_logged_in   
def create_at():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        author = request.form['author']
        print(author)
        data = mymongo.insert_data(title,desc,author)
        print(data)
        return redirect('/list')   
    elif request.method == 'GET':
        return render_template('dashboard.html')
    
@app.route('/del/<ids>')
def delete(ids):
    mymongo.del_data(ids)
    return redirect('/list')


@app.route('/edit/<ids>', methods=['GET','POST'])    
def edit_list(ids):
    if request.method == 'GET':
        data = mymongo.find_one_data(ids)
        # print(data)
        # return "success"
        return render_template('edit.html', data=data)
    elif request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        mymongo.update_data(ids, title, desc)
        return redirect('/list')




if __name__== "__main__":
    app.run(debug=True, port=9999)