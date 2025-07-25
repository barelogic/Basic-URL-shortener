from flask import Flask,request,redirect,render_template,url_for,flash
import sqlite3,os,random,string

app=Flask(__name__)
app.secret_key="supersecretkey"
DB_FILE="url_shortener.db"

def init_db():
    if not os.path.exists(DB_FILE):
        conn=sqlite3.connect(DB_FILE)
        c=conn.cursor()
        c.execute('''
                  CREATE TABLE URLs (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  short_code TEXT UNIQUE NOT NULL,
                  original_url TEXT NOT NULL
                  )
                  ''')
        conn.commit()
        conn.close()
init_db()

def generate_code(length=6):
    chars=string.ascii_letters+string.digits
    return ''.join(random.choices(chars,k=length))

@app.route('/',methods=["POST","GET"])
def index():
    if request.method== "POST":
        original_url=request.form.get('url')
        if not original_url:
            flash("Please enter a URL.","error")
            return render_template('index.html')
        
        conn=sqlite3.connect(DB_FILE)
        c=conn.cursor()
        while True:
            code=generate_code()
            c.execute("SELECT 1 FROM URLs WHERE short_code=?", (code,))
            if not c.fetchone():
                break

        c.execute("INSERT INTO urls (short_code, original_url) VALUES (?, ?)", (code, original_url))
        conn.commit()
        conn.close()

        short_url = request.host_url + code
        return render_template('index.html', short_url=short_url)

    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_original(short_code):
    conn=sqlite3.connect(DB_FILE)
    c=conn.cursor()
    c.execute("SELECT original_url FROM URLs WHERE short_code= ?", (short_code,))
    row=c.fetchone()
    conn.close()

    if row:
        return redirect(row[0])
    else:
        return "invalid short URL",404

def main():
    app.run(host="0.0.0.0",port=5000,debug=False)

main()