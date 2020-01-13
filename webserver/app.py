from flask import Flask
from flask import *
import requests
import time
import pdb


app = Flask(__name__, static_folder="static")

@app.route('/', methods=['GET', 'POST'])
def index():
    response = requests.get("http://0.0.0.0:4444/&&/")
    data = response.json()
    machine = []
    uptime = []

    for user in data:
        for couple in data[user]:
            for key, value in couple.items():
                if 'uname' in key:
                    machine.append(value)
                if 'uptime' in key:
                    uptime.append(value)

    print(machine)
    print(uptime)
    return render_template('index.html', machine=machine, uptime=uptime, user=user)

def main():
    app.run(host="localhost", debug=True)
main()