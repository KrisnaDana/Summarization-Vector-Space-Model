from flask import Flask, render_template, request
import summary

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    judul = request.form['judul']
    teks = request.form['teks']
    # tes = summary.main(judul, teks)
    return f"{judul}, {teks}!"