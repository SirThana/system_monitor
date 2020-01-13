from flask import Flask
from flask import *
import requests
import time
import pdb


app = Flask(__name__, static_folder="static")

@app.route('/', methods=['GET', 'POST'])
def index():
    response = requests.get("http://0.0.0.0:8888/&&/")
    data = response.json()
    machine = []
    uptime = []
    user = []

    for who in data:
        user.append(who)
        for couple in data[who]:
            for key, value in couple.items():
                if 'uname' in key:
                    machine.append(value)
                if 'uptime' in key:
                    uptime.append(value)

    print(machine)
    print(uptime)
    return render_template('index.html', user=user, machine=machine, uptime=uptime)

def main():
    app.run(host="localhost", debug=True)
main()