from flask import Flask , Blueprint , redirect , url_for , render_template , request , session , flash , send_file
import os 
from models import Files 
import datetime

UPLOAD_FOLDER = f'{os.getcwd()}/static/'
ALLOWED_EXTENSIONS = {'rar' , 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' , 'exe' , 'py' , 'js' , 'cs' , 'cpp' , 'ahk' , 'zip' , 'csv' , 'xlsx' , 'mp4' , 'json' , 'html' , 'ico' , 'dll' , 'dat'}

file = Blueprint('file' , __name__ , template_folder='templates' , static_folder='static')

def log(url):
    with open('logs/access_log.txt' , 'a') as f:
        now = datetime.datetime.now()
        date_and_time = now.strftime('%d/%m/%Y %H:%M:%S')
        try:
            f.write(f"\n[{date_and_time}] {url} Accessed By {request.environ['HTTP_X_FORWARDED_FOR']}")
        except:
            f.write(f"\n[{date_and_time}] {url} Accessed By Unkown")

@file.route('/video/<code>')
def view_video(code):
    log(f'/file/video/{code}')
    if Files('' , code).check_if_code_exist():
        ext = Files.get_file_info(code)[0][0].split('.')[1]
        filename = Files.get_file_info(code)[0][0]
        if ext == 'mp4':
            return render_template('video_page.html' , filename=filename , code=code , error = False)
        else:
            return render_template('video_page.html' , filename=filename, code=code , error = True)

    return redirect('/')

@file.route("/image/<code>")
def view_image(code):
    log(f'/file/image/{code}')
    if Files('' , code).check_if_code_exist():
        ext = Files.get_file_info(code)[0][0].split('.')[1]
        filename = Files.get_file_info(code)[0][0]
        if ext == 'png' or ext == 'jpg' or ext == 'jpeg':
            return render_template('image_page.html' , filename=filename , code=code , error = False)
        else:
            return render_template('image_page.html' , filename=filename , code=code , error = True)

    return redirect('/')

@file.route("<code>")
def see_download(code):
    log(f'/file/{code}')
    if Files('' , code).check_if_code_exist():
        filename = Files.get_file_info(code)[0][0]
        size = os.path.getsize(f'{UPLOAD_FOLDER}{Files.get_file_info(code)[0][0]}')
        size = size/1000000
        
        return render_template('download_page.html' , filename=filename , size=size , code=code)

    else:
        return redirect('/database')

@file.route("/download/<code>")
def download(code):
    log(f'file/download/{code}')
    if Files('' , code).check_if_code_exist():
        filename = Files.get_file_info(code)[0][0]
        path=f'{UPLOAD_FOLDER}{filename}'
        with open('logs/download_log.txt' , 'a') as f:
            now = datetime.datetime.now()
            date_and_time = now.strftime('%d/%m/%Y %H:%M:%S')
            try:
                f.write(f"\n[{date_and_time}] {filename} Downloaded From {request.environ['HTTP_X_FORWARDED_FOR']}")   
            except:
                f.write(f"\n[{date_and_time}] {filename} Downloaded From Unkown")
        return send_file(path, as_attachment=True)

    else:
        return redirect('/database')
