from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

recs = []


@app.route("/")
def hello_word():
    return render_template('index.html', recs=recs)


@app.route("/entry", methods=['POST'])
def add_entry():
    if request.method == 'POST':
        video_path = request.form['path']
        time_str = request.form['time']
        idx = request.form['index']

        print(video_path, time_str, idx)
        recs.append(video_path)
        return "added"
    else:
        return redirect(url_for('/'))
