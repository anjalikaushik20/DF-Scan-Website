from flask import Flask, render_template, request
import cgitb
import os
import shutil
from sklearn import preprocessing; cgitb.enable()
# import cgi
import python.dataPrep as dp

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/scan", methods=['POST'])
def scan():
    # form = cgi.FieldStorage()
    # fileitem = form.getvalue('fileName')
    _fileitem = request.files.get('fileName')

    name = _fileitem.filename.split('.')[0]

    if _fileitem:
        _fileitem.save(f'videos/{name}.mp4')
        message = 'The file was uploaded successfully'
    else:
        message = 'No file was uploaded'

    
    print(message)
    print(_fileitem)

    #passing for preprocessing
    output = dp.dataProcess(name)
    
    #deleting directories
    print('Deleting files...')
    os.remove(f'videos/{name}.mp4')
    shutil.rmtree(f'videos/{name}/')
    print('Files deleted after detection!')

    return render_template('index.html', result = '{}'.format(output))


if __name__=="main":
    app.run(debug=True)