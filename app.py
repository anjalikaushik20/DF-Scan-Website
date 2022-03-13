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
    return render_template('index.html', loading = '{}'.format("Loading!"))

@app.route("/scan", methods=['POST'])
def scan():
    # form = cgi.FieldStorage()
    # fileitem = form.getvalue('fileName')
    # _fullname = _fileitem.filename
    
    _fileitem = request.files.get('fileName')
    
    if _fileitem:
        name = _fileitem.filename.split('.')[0]
        extension = _fileitem.filename.split('.')[1]
        if extension == 'mp4':
            _fileitem.save(f'videos/{name}.mp4')
            message = 'The file was uploaded successfully'
        else:
            return render_template('result.html', result = '{}'.format('Error: Not an mp4 file!'), loading = '{}'.format(" "))
    else:
        message = 'No file was uploaded'
        output = 'No file was uploaded. Try Again!'
        return render_template('result.html', result = '{}'.format(output))

    
    print(message)
    print(_fileitem)
    # print(_fullname)

    #passing for preprocessing
    output = dp.dataProcess(name)

    #deleting directories
    print('Deleting files...')
    os.remove(f'videos/{name}.mp4')
    shutil.rmtree(f'videos/{name}/')
    print('Files deleted after detection!')

    return render_template('result.html', result = '{}'.format(output), loading = '{}'.format(" "))
        
    


if __name__=="main":
    app.run(debug=True)