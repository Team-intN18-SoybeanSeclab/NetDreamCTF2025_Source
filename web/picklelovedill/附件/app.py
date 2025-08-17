# Have fun!
import os
import mimetypes
import dill

from bottle import Bottle, run, request, template, response
from base64 import b64encode
app = Bottle()
UPLOAD_DIR = os.path.abspath('./uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)
class chal():
    # flag here
    pass

INDEX_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>文件管理</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        form { margin-bottom: 20px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
        input[type="file"], input[type="text"] { margin: 10px 0; }
        .message { color: green; margin: 10px 0; }
        .error { color: red; }
    </style>
</head>
<body>
    <div class="container">
        <h1>文件上传</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" />
            <input type="submit" value="上传" />
        </form>

        <h1>文件读取</h1>
        <form action="/read" method="get">
            <input type="text" name="filename" placeholder="输入文件名" required />
            <input type="submit" value="读取" />
        </form>

        % if message:
            <div class="message">{{message}}</div>
        % end
        % if error:
            <div class="error">{{error}}</div>
        % end
    </div>
</body>
</html>
'''

def render_template(message='', error=''):
    return template(INDEX_TEMPLATE, message=message, error=error)

@app.route('/')
def index():
    return render_template()

@app.post('/upload')
def upload_file():
    upload = request.files.get('file')
    
    if not upload:
        return render_template(error='请选择要上传的文件')
    if '..' in upload.filename:
        return render_template(error='不要透我！>_<')
    filename = os.path.basename(upload.filename)
    if not filename:
        return render_template(error='无效的文件名')

    save_path = os.path.join(UPLOAD_DIR, filename)
    try:
        upload.save(save_path, overwrite=True)
    except Exception as e:
        return render_template(error=f'上传失败: {str(e)}')
    
    return render_template(message=f'文件 {filename} 上传成功！')

@app.get('/read')
def read_file():
    filename = request.query.get('filename', '').strip()
    if not filename:
        return render_template(error='请输入文件名')
    if '..' in filename:
        return render_template(error='不要透我！>_<')
    safe_name = os.path.basename(filename)
    if not safe_name:
        return render_template(error='无效的文件名')

    file_path = os.path.join(UPLOAD_DIR, safe_name)
    
    if not os.path.exists(file_path):
        return render_template(error='文件不存在')
    
    if not os.path.isfile(file_path):
        return render_template(error='请求的不是有效文件')

    mime_type, _ = mimetypes.guess_type(file_path)
    response.content_type = mime_type or 'application/octet-stream'
    
    try:
        with open(file_path, 'rb') as f:
            content = f.read().decode(errors='replace')
        try:
            challenge = b64encode(dill.dumps(chal())).decode()
            blacklist = dir(__builtins__)
            blacklist += dir([])
            blacklist += dir(1)
            blacklist += dir(())
            blacklist += dir(True)
            blacklist += dir('NO HACKER')
            # I'm pretty sure nothing can be done now ;) 
            # Even if i do not ban dicts, but, u know, is it too complex to SSTI with {} and without almost every magic methods?
            # Here is a hint if you really get stuck:
            # dHJ5IHRvIGV4cGxvaXQgd2l0aCBzb21ldGhpbmcgdW5pcXVlIHRvIGJvdHRsZSA+Xzw=
            for i in blacklist:
                if i in content:
                    return 'STOP HACKING!'
            return template(f'''% import pickle
                            % setdefault('chal', '{challenge}')
The content is: ''' + content) # Yeah I don’t know why but rendering it is so f**king fun! XD
        except:
            import traceback
            traceback.print_exc()
            return content
    except Exception as e:
        return render_template(error=f'文件读取失败: {str(e)}')

if __name__ == '__main__':
    run(app, host='localhost', port=5000, debug=True, reloader=True)
