from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/scan", methods=['POST'])
def scan():
    output = "Rake"

    return render_template('index.html', result = '{}'.format(output))


if __name__=="main":
    app.run(debug=True)