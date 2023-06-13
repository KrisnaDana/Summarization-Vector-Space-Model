from flask import Flask, render_template, request
import jaccard
import tf_idf

# flask --debug run
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def submit():
    title = request.form['judul']
    text = request.form['teks']
    count = request.form['jumlah']
    # result = jaccard.main(title, text, count)
    result = tf_idf.main(title, text, count)
    return render_template('index.html', judul=title, teks=text, jumlah=count, hasil=result)