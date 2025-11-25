import os
import subprocess
from flask import Flask, request

app = Flask(__name__)

@app.route("/ping")
def ping():
    ip = request.args.get("ip")
    os.system(f"ping -c 1 {ip}")  # Command Injection vulnerability
    return "Ping executed!"

@app.route("/run")
def run():
    cmd = request.args.get("cmd")
    subprocess.call(cmd, shell=True)  # RCE vulnerability
    return "Command executed!"
