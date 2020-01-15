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
    return render_template('index.html', data=data)

def main():
    app.run(host="localhost", debug=True) #Default port 5000
main()
