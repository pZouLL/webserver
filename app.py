from flask import Flask , Blueprint , redirect , url_for , render_template , request , session , flash
import os
from datetime import timedelta
import datetime

from database import database
from auth import auth 
from file import file

def log(url):
    with open('logs/access_log.txt' , 'a') as f:
        now = datetime.datetime.now()
        date_and_time = now.strftime('%d/%m/%Y %H:%M:%S')
        try:
            f.write(f"\n[{date_and_time}] {url} Accessed By {request.environ['HTTP_X_FORWARDED_FOR']}")
        except:
            f.write(f"\n[{date_and_time}] {url} Accessed By Unkown")
 

app = Flask(__name__)

app.permanent_session_lifetime = timedelta(minutes = 5)
app.secret_key = "j0dWQHFE*(Hgh434g9werSGLhg40eglxkdhg0"

app.register_blueprint(database , url_prefix='/database')
app.register_blueprint(auth , url_prefix = '/authenticate')
app.register_blueprint(file , url_prefix = '/file')

@app.route("/")
def home():
    log('/')
    if 'logged_in' in session:
        return render_template("home.html")
    else:
        return redirect('/authenticate/login')


if __name__ == '__main__':
    app.run(debug=True , host='192.168.20.105')