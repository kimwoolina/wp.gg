from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import jwt

# Flask 애플리케이션 초기화
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins='*')

# 사용자 정보를 저장
users = {}

# 메인 페이지 라우트
@app.route('/')
def index():
    return render_template('index.html')

# 로그인 엔드포인트
@app.route('/login/', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    if username:
        token = jwt.encode({'username': username}, app.config['SECRET_KEY'], algorithm='HS256')
        users[username] = token
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid username'}), 400

# WebSocket 연결 
@socketio.on('connect')
def handle_connect():
    print('Client connected')

# WebSocket 메시지 
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

# WebSocket 연결 해제 
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# 5001서버 실행
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
