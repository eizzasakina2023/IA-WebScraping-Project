import os
import json
import sqlite3
import subprocess
from flask import Flask, request, send_file, make_response

app = Flask(__name__)

# --- Basic routes ---

@app.route("/")
def home():
    name = request.args.get("name", "Guest")
    # XSS vulnerability (reflected output)
    return f"<h2>Welcome {name}</h2>"

@app.route("/file")
def get_file():
    path = request.args.get("path", "")
    # Directory Traversal
    return send_file(path)

# --- System interaction ---

@app.route("/ping")
def ping():
    ip = request.args.get("ip")
    os.system(f"ping -c 1 {ip}")   # Command Injection
    return "Done"

@app.route("/run")
def run():
    cmd = request.args.get("cmd")
    subprocess.call(cmd, shell=True)   # RCE
    return "Executed"

# --- Database operation ---

@app.route("/user")
def user_lookup():
    username = request.args.get("u", "")
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    # SQL query without sanitization
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cur.execute(query)
    data = cur.fetchall()
    conn.close()
    return str(data)

# --- Unsafe JSON deserialization ---

@app.route("/config", methods=["POST"])
def config():
    raw = request.data.decode()
    # unsafe use of json.loads for untrusted input
    settings = json.loads(raw)
    return settings.get("status", "ok")

# --- Cookie reflection (XSS) ---

@app.route("/profile")
def profile():
    user = request.cookies.get("user", "anonymous")
    resp = make_response(f"<div>User: {user}</div>")  # XSS via cookie
    return resp


if __name__ == "__main__":
    app.run()
