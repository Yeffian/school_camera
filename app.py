from flask import Flask, render_template

app = Flask(__name__)

todos = {
    'foo': 'bar',
    'baz': 'kaz',
    'elon': 'musk'
}

@app.route("/")
def hello_word():
    return render_template('index.html', todos=todos)