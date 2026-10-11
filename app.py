from flask import Flask
import os, psycopg2

app = Flask(__name__)

@app.route("/")
def home():
    return "Student Notes App is running"

@app.route("/health")
def health():
    return "ok", 200

@app.route("/db")
def db():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    conn.close()
    return "database connected"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
