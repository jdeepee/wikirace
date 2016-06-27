from flask import Flask, render_template, request, send_from_directory, session
from threading import Thread
from flask_socketio import SocketIO, emit, send, join_room, rooms, disconnect
from MySQLdb import connect

# cnx = connect(user='root',
#               passwd='wikiracetea',
#               host='cp-0627-1.hbtn.io',
#               port=3306,
#               db='wikirace',
#               charset='utf8',
#               )
#
# cursor = cnx.cursor()

add_data = ("INSERT INTO Requests "
               "(id, first_word, second_word) "
               "VALUES (%s, %s, %s)")

app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading")

@app.route('/')
@app.route('/index')
@app.route('/index.html')
@app.route('/index.htm')
@app.route('/index.php')
def index():
	return render_template("index.html")

@socketio.on('hello')
def hello(data):
    join_room(data['id'])

    socketio.emit("loaded", room=data["id"])

    #start thread with callback
    t = Thread(target=get_path, args=(data, finished))
    t.start()

    # data = (data['id'], data['first_word'], data['second_word'])
    # cursor.execute(add_data, data)

def get_path(data, finished):
    path = [
        data["word_1"],
        "filler",
        "test",
        "bears",
        data["word_2"],
    ]
    finished(path, data["id"])
    return path

def finished(path, room):
    socketio.emit("done", path, room=room)

if __name__ == "__main__":
    socketio.run(app)
