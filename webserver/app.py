from flask import Flask
from flask import *

#mydb = mysql.connector.connect(
#host="192.168.157.130",
#user="admin",
#passwd="Welkom123!",
#database="users"
#)


app = Flask(__name__, static_folder="static")

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', name='index')

def main():
    app.run(host="localhost", debug=True)
main()