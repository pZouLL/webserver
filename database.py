from flask import Flask , Blueprint , redirect , url_for , render_template , request , session , flash , send_file , jsonify
from werkzeug.utils import secure_filename
import random
from models import Files
import os
import datetime

def log(url):
    with open('logs/access_log.txt' , 'a') as f:
        now = datetime.datetime.now()
        date_and_time = now.strftime('%d/%m/%Y %H:%M:%S')
        try:
            f.write(f"\n[{date_and_time}] {url} Accessed By {request.environ['HTTP_X_FORWARDED_FOR']}")
        except:
            f.write(f"\n[{date_and_time}] {url} Accessed By Unkown")

database = Blueprint('database' , __name__ , template_folder='templates' , static_folder='static')

UPLOAD_FOLDER = f'{os.getcwd()}/static/'
ALLOWED_EXTENSIONS = {'rar' , 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' , 'exe' , 'py' , 'js' , 'cs' , 'cpp' , 'ahk' , 'zip' , 'csv' , 'xlsx' , 'mp4' , 'json' , 'html' , 'ico' , 'dll' , 'dat'}

@database.route("/")
def view_database(): 
    log('/database')
    if 'logged_in' in session:
        all_files = Files.get_all_db()
        return render_template("database.html" , all_files=all_files)
    else:
        return redirect('/authenticate/login')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@database.route('/<code>')
def database_info(code):
    log(f'/database/{code}')
    if 'logged_in' in session:
        if Files('' , code).check_if_code_exist():
            filename = Files.get_file_info(code)[0][0].split('.')[0]
            code = Files.get_file_info(code)[0][1]
            ext = Files.get_file_info(code)[0][0].split('.')[1]
            size = os.path.getsize(f'{UPLOAD_FOLDER}{Files.get_file_info(code)[0][0]}')
            size = size/1000000

            return render_template('database_info.html' , filename = filename , code = code , ext = ext , size = size)
        
        else:
            return redirect('/')
        
    else:
        return redirect('/authenticate/login')

@database.route("/delete/<code>" , methods=['POST' , 'GET'])
def delete(code):
    log(f'/database/delete/{code}')
    if 'logged_in' in session:
        if Files('' , code).check_if_code_exist():
            filename = Files.get_file_info(code)[0][0]
            os.remove(f'{UPLOAD_FOLDER}{filename}')
            Files('' , code).delete()
            return redirect("/database")
    else:
        return redirect('/authenticate/login')



@database.route("/create-file" , methods=['POST','GET'])
def create_database(): 
    log('/database/create-file')
    if 'logged_in' in session:
        if request.method == 'POST':
            if 'file' not in request.files:
                return redirect('create_file')
            file = request.files['file'] 
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = filename.replace(" " , "_").replace("/" , "")
                char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'



                while True:
                    code = ''.join(random.sample(char , 32))
                    check_code = Files(filename , code)
                    if check_code.check_if_code_exist():
                        continue 
                    else:
                        break
                
                thing = 0
                while True:
                    thing += 1
                    if check_code.check_if_name_exist():
                        print(check_code.get_filename())
                        print(check_code.get_code())
                        name = filename.split(".")[0]
                        ext = filename.split(".")[1]
                        check_code = Files(f'{name}({thing}).{ext}' , code)
                        filename = check_code.get_filename()
                        print(check_code.get_filename())

                    else:
                        break

                file.save(os.path.join(f'{UPLOAD_FOLDER}{filename}'))
                check_code.save_to_db()
                now = datetime.datetime.now()
                date_and_time = now.strftime('%d/%m/%Y %H:%M:%S')
                with open('logs/upload_log.txt' , 'a') as f:
                    f.write(f"\n[{date_and_time}] {filename} Uploaded")   
                return redirect(url_for('database.view_database'))
        else:
            return render_template("create_file.html")  


    return redirect('/authenticate/login')
    
