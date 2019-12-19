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
            host="192.168.157.130",
            user="admin",
            passwd="Welkom123!",
            database="statistics")
            cursor = mydb.cursor()
            getUptime = "SELECT * FROM statistics;"
            cursor.execute(getUptime)
            uptime = cursor.fetchall()
            print(uptime)
            lastTime = time.time()
            return render_template('index.html', data=uptime)

def main():
    app.run(host="localhost", debug=True)
main()