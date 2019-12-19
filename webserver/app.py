from flask import Flask
from flask import *
import mysql.connector
import time
import pdb


app = Flask(__name__, static_folder="static")

@app.route('/', methods=['GET', 'POST'])
def index():
    lastTime = time.time()
    print(lastTime)
    while True:
        currentTime = time.time()
        difference = currentTime - lastTime
        if difference > 1:
            mydb = mysql.connector.connect(
            host="145.109.164.133",
            user="tester",
            passwd="P@ssword",
            database="TESTMAU")
            cursor = mydb.cursor()
            getUptime = "SELECT * FROM Data;"
            cursor.execute(getUptime)
            uptime = cursor.fetchall()
            print(uptime)
            lastTime = time.time()
            return render_template('index.html', data=uptime)

def main():
    app.run(host="localhost", debug=True)
main()