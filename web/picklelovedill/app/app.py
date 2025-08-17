import os
import mimetypes
import dill

from bottle import Bottle, run, request, template, response
from base64 import b64encode
app = Bottle()
UPLOAD_DIR = os.path.abspath('./uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)
# flag{B0ttl3_❤_pickle_and_watch_this_https://www.bilibili.com/video/BV1GJ411x7h7}
# HOW COULD YOU GET THE SOURCE CODE???? PLZ CONTECT QQ:1372449351 PLZPLZPLZ
# YOU ARE TRUELY A SSTI MASTER
class chal ():#line:1
    def __init__ (OOOOO0OO0O00OO000 ,O0O0O0O00OO0O0OO0 ,OO0OO00000O00O0OO ,OO0OOOO00OOOOOO00 ):#line:2
        print ('Okay you are SSTI master, well done :)\nBut now, the flag is hidden in this object, find it out!\n Good Luck!')#line:3
        print ('Yeah here is a present. Part1 of the flag is flag{B0tt')#line:4
    def __hash__ (OO000OO0OO0O0OO0O ):#line:5
        import base64 #line:6
        _OO0OO0O00000000OO ='wdvMxo/fzN3TnZWP25LOTQgDzt/EwtrbwM7M'#line:7
        OOOO0000OO00OO00O =_OO0OO0O00000000OO .encode ('utf-8')#line:8
        O00OO000OO0OOOOO0 =base64 .b64decode (OOOO0000OO00OO00O )#line:9
        OO0OOOO0OO0O00O00 =bytes (O0O00OO0OOOOOO0O0 ^0xAA for O0O00OO0OOOOOO0O0 in O00OO000OO0OOOOO0 )#line:10
        OOOO0O00OO0O0O0OO =bytes ((OO00OOO00OOOO0O0O -5 )%256 for OO00OOO00OOOO0O0O in OO0OOOO0OO0O00O00 )#line:11
        return OOOO0O00OO0O0O0OO .decode ('utf-8')#line:12
    def __eq__ (O0OOO0O0000O00OOO ,O00O0O00OOOO0OOOO ):#line:13
        import base64 #line:14
        _OOO00OOO00OOOO0O0 ='LSsmLGfXJtHTEBln1SMk3CbTIC8k0y8u0CQv'#line:15
        OO00OO0O00OOOO000 =_OOO00OOO00OOOO0O0 .encode ('utf-8')#line:16
        OOO000OO0O0O000O0 =base64 .b64decode (OO00OO0O00OOOO000 )#line:17
        OO0O0O0O000O00OO0 =bytes (O0O0O0O0OO0OOO0OO ^0x55 for O0O0O0O0OO0OOO0OO in OOO000OO0O0O000O0 )#line:18
        O000O000OOO0O00O0 =bytes ((OOOOOOO000O0OOOOO -18 )%256 for OOOOOOO000O0OOOOO in OO0O0O0O000O00OO0 )#line:19
        return O000O000OOO0O00O0 .decode ('utf-8')#line:20
    def __fake__ (OOO00OO0O000OOO00 ,flag_part_4 ='ttps://www.bilibili.co'):#line:22
        ""#line:25
        import base64 #line:26
        _OOOO0O0O00O0O0000 ='+f8E+kPzBPX3KS1DNzQ06yr7KuA='#line:27
        O0OOO00OO0OOO0000 =_OOOO0O0O00O0O0000 .encode ('utf-8')#line:28
        OO00O0O0OO000OOO0 =base64 .b64decode (O0OOO00OO0OOO0000 )#line:29
        O000OOO0O00OO000O =bytes (OO00O0O0OOOOO0000 ^0x78 for OO00O0O0OOOOO0000 in OO00O0O0OO000OOO0 )#line:30
        OO0000O000O0OOOO0 =bytes ((O0OO0O000OO000000 -27 )%256 for O0OO0O000OO000000 in O000OOO0O00OO000O )#line:31
        return OO0000O000O0OOOO0 .decode ('utf-8')
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
    if '../' in upload.filename:
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
    if '../' in filename:
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
            challenge = b64encode(dill.dumps(chal(1,2,3))).decode()
            blacklist = dir(__builtins__)
            blacklist += dir([])
            blacklist += dir(1)
            blacklist += dir(())
            blacklist += dir(True)
            blacklist += dir('NO HACKER')
            blacklist += dir({})
            # I'm pretty sure nothing can be done now ;) 
            # Even if i do not ban dicts, but, u know, is it too complex to SSTI with {} and without almost every magic methods?
            # try to exploit with something unique to bottle >_<        
            for i in blacklist:
                if i or '{{chal}}' or ' ' in content:
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
