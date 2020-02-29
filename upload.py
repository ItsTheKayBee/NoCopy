from flask import *
import mysql.connector
import time
import hasher

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="nocopy"
        )
        f = request.files['uploaded-file']
        file_name=f.filename
        ext=f.filename.split(".")[-1]
        mycursor = mydb.cursor()
        ts=time.time()
        sql=''
        val=''
        path="files/"+file_name
        if ext == 'txt':
            sql = "INSERT INTO docs (path, time, hashval, type) VALUES (%s, %s,%s,%s)"
            val = (path,ts, hasher.txt_hash(), ext)
        elif ext == 'docx' or ext == 'doc':
            sql = "INSERT INTO docs (path, time, hashval, type) VALUES (%s, %s,%s,%s)"
            val = (path,ts, hasher.word_hash(), ext)
        elif ext == 'pdf':
            sql = "INSERT INTO docs (path, time, hashval, type) VALUES (%s, %s,%s,%s)"
            val = (path,ts,hasher.pdf_hash(),ext)
        elif ext == 'mp3':
            sql = "INSERT INTO music (path, time, hashval) VALUES (%s, %s,%s)"
            val = (path,ts,hasher.audio_hash())
        elif ext == 'jpg' or ext == 'png':
            sql = "INSERT INTO pics (path, time, hashval) VALUES (%s, %s,%s)"
            val = (path,ts,hasher.image_hash())

        mycursor.execute(sql, val)

        mydb.commit()
        f.save(path)
        return render_template("success.html", name=f.filename)


@app.route('/upload')
def upload():
    return render_template("upload.html")


@app.route('/pics')
def pics():
    return render_template("pics.html")


@app.route('/music')
def music():
    return render_template("music.html")


@app.route('/text')
def text():
    return render_template("text.html")


@app.route('/pdf')
def pdf():
    return render_template("pdf.html")


@app.route('/word')
def word():
    return render_template("word.html")


if __name__ == '__main__':
    app.run(debug=True)