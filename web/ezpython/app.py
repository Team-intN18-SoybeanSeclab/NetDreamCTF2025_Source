from flask import Flask, request, Response, render_template_string

app = Flask(__name__)

FLAG = open('/flag').read().strip()

@app.route('/')
def stage1():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <src
        <title></title>
        <!-- ：/s3c0nd -->
    </head>
    </html>
    """

@app.route('/s3c0nd')
def stage2():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>S3c0nd</title>
    </head>
    <body>
        <h1>only fuzz(number)</h1>
    </body>
    </html>
    """

@app.route('/114514')
def stage3():
    name = request.args.get('name', 'guest')

    template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>野兽先辈の住所</title>
    </head>
    <body>
        <h1>你好 {name}！</h1>
        <!-- 听说访问该页面的某get参数的某个数值可以爆源码 -->
    </body>
    </html>
    """

    if request.args.get('source') == '6969':
        with open(__file__, 'r', encoding="latin-1") as f:
            return Response(f.read(), mimetype='text/plain')

    return render_template_string(template, name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
