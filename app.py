import eventlet
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send, emit
import jwt
from chats.models import db, User  # DB와 모델 임포트 필요시
import config

# Flask 앱 생성 및 설정
app = Flask(__name__)
app.config.SECRET_KEY  # JWT 토큰 생성을 위한 시크릿 키

# SocketIO 객체 생성 - CORS 허용 (다른 도메인에서 접근할 수 있도록 설정)
socketio = SocketIO(app, cors_allowed_origins='*')

# 사용자 로그인 엔드포인트
@app.route('/login/', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')  # 클라이언트에서 전달된 username
    if username:
        # JWT 토큰 생성
        token = jwt.encode({'username': username}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})  # JWT 토큰을 클라이언트로 반환
    return jsonify({'error': 'Invalid username'}), 400  # username이 없을 경우 에러 반환

# WebSocket 연결 시 실행
@socketio.on('connect')
def handle_connect():
    print('Client connected')  # 클라이언트가 연결됐을 때 콘솔에 출력

# WebSocket으로부터 메시지를 받을 때 실행
@socketio.on('message')
def handle_message(data):
    token = data.get('sender')  # 클라이언트에서 보낸 JWT 토큰 (발신자 정보)
    message = data.get('message')  # 클라이언트에서 보낸 메시지 내용
    if token and message:
        try:
            # JWT 토큰 검증 및 디코딩
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            # 발신자 정보 추출
            sender = decoded_token.get('username')  
            # 클라이언트에 메시지 전송 (모든 클라이언트에 브로드캐스트)
            emit('message', {'message': message, 'sender': sender}, broadcast=True)
        except jwt.InvalidTokenError:
            print('Invalid token')  # 토큰이 유효하지 않을 경우

# WebSocket 연결 해제 시 실행
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')  # 클라이언트가 연결 해제됐을 때 콘솔에 출력

# 기본 페이지 라우팅 (index.html을 클라이언트에 전달)
@app.route('/')
def index():
    return render_template('index.html')

# 5001서버 실행
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
