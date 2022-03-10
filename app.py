from flask import Flask, render_template, request
import cgitb; cgitb.enable()
# import cgi

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/scan", methods=['POST'])
def scan():
    # form = cgi.FieldStorage()
    # fileitem = form.getvalue('fileName')
    fileitem = request.files.get('fileName')

    name = fileitem.filename.split('.')[0]

    if fileitem:
        fileitem.save(f'videos/{name}.mp4')
        message = 'The file was uploaded successfully'
    else:
        message = 'No file was uploaded'

    output = "Rake"
    print(message)
    print(fileitem)

    return render_template('index.html', result = '{}'.format(output))


if __name__=="main":
    app.run(debug=True)