# -- coding: UTF-8 --

'''
地铁项目——上传文件并解析
'''

import os
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'   #UPLOAD_FOLDER 是我们储存上传的文件的地方
ALLOWED_EXTENSIONS = set(['txt', 'csv'])  #ALLOWED_EXTENSIONS 则是允许的文件类型的集合

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  #把上传文件限制为最大 20 MB    如果请求传输一个更大的文件， Flask 会抛出一个 RequestEntityTooLarge 异常。

app.config.update(dict(
    SECRET_KEY='development key'
))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    '检查文件类型是否有效、上传通过检查的文件、以及将用户重定向到 已经上传好的文件 URL 处'
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # print os.path.join(app.config['UPLOAD_FOLDER'], filename)
            return redirect(url_for('analysis_file', filename=filename))
    return render_template('index.html')


@app.route('/uploads/<filename>')
def analysis_file(filename):
    #'分析文件'
    import skitlearn_calculate
    cal = skitlearn_calculate.calculate(filename)
    x1, x2, x3 = cal.Divide_data()
    result = []
    result.append(cal.Lasso(x1, num='1'));result.append(cal.Lasso(x2, num='2'));result.append(cal.Lasso(x3, num='3'))
    print request.url
    return render_template('index.html', show_result=result)

