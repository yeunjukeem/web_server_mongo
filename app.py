# app.py_web_server_mongo

from flask import Flask, render_template, request
from data import Articles
from models import MyMongo
from config import MONGODB_URL

app = Flask(__name__)

mymongo = MyMongo(MONGODB_URL , 'os')

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
        mymongo.user_insert(username , email , phone , password)

        print(username , email , phone , password)
        return "success"
        

    
    
   

if __name__== "__main__":
    app.run(debug=True, port=9999)