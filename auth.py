from flask import Flask , Blueprint , redirect , url_for , render_template , request , session , flash
import hashlib
from models import VerifyUser
import datetime

auth = Blueprint('auth' , __name__ , template_folder='templates' , static_folder='static')

def log(url):
    with open('logs/access_log.txt' , 'a') as f:
        now = datetime.datetime.now()
        date_and_time = now.strftime('%d/%m/%Y %H:%M:%S')
        try:
            f.write(f"\n[{date_and_time}] {url} Accessed By {request.environ['HTTP_X_FORWARDED_FOR']}")
        except:
            f.write(f"\n[{date_and_time}] {url} Accessed By Unkown")

@auth.route("/login" , methods = ['POST' , 'GET'])
def login():
    log('/login')
    if request.method == "POST":
        username = str(request.form["user"])
        hashed_pwd = hashlib.sha256(request.form["password"].encode('utf-8')).hexdigest()
        user = VerifyUser(username , hashed_pwd)
        logged_in = user.verify()
        print(logged_in)
        if logged_in:
            session['logged_in'] = "YES" 
            return redirect('/')
    return render_template('login.html')

@auth.route("/logout")
def logout():
    log('authenticate/logout')
    if 'logged_in' in session:
        session.pop('logged_in' , None)
    return redirect("/authenticate/login")