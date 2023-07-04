from flask import Flask, render_template, request
import jaccard
import tf_idf
import svd
import time

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

    start_time = time.time()

    result = jaccard.main(title, text, count)
    # result = tf_idf.main(title, text, count)
    # result = svd.main(title, text, count) # SVD (Singular Value Decomposition)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Tampilkan lama waktu proses
    print(f"Lama waktu proses: {elapsed_time} detik")

    return render_template('index.html', judul=title, teks=text, jumlah=count, hasil=result)