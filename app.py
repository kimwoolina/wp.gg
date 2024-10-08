from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# 홈 페이지 렌더링
@app.route('/')
def index():
    return render_template('index.html')


# 클라이언트가 웹소켓에 연결되었을 때
@socketio.on('connect')
def handle_connect():
    print('Client connected')

# 클라이언트가 메시지를 보냈을 때 처리
@socketio.on('message')
def handle_message(msg):
    print(f"Received message: {msg}")
    send(f"Message received: {msg}", broadcast=True)

# 클라이언트가 연결을 끊었을 때
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
