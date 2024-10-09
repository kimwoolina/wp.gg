from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send, emit
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins='*')

users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    if username:
        token = jwt.encode({'username': username}, app.config['SECRET_KEY'], algorithm='HS256')
        users[username] = token
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid username'}), 400

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('message')
def handle_message(data):
    token = data.get('sender')
    message = data.get('message')
    if token and message:
        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            sender = decoded_token.get('username')
            emit('message', {'message': message, 'sender': sender}, broadcast=True)
        except jwt.InvalidTokenError:
            print('Invalid token')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
