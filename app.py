from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, send
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'django-insecure-uw(g7z_f!7siyl7#on=!r=+#*izdigx8c&rj&iv)@zg(%al-gp'  # JWT 생성에 사용할 시크릿 키
socketio = SocketIO(app)  # SocketIO 설정

# 로그인 엔드포인트
@app.route('/login/', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 사용자 인증 (간단하게 비밀번호가 'password'인 경우로 가정)
    if password == 'password':
        # JWT 토큰 생성
        token = jwt.encode({
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# 루트 경로로 접속하면 index.html 렌더링
@app.route('/')
def index():
    return render_template('index.html')  # templates 폴더 안의 index.html 파일 렌더링

# WebSocket 메시지 처리
@socketio.on('message')
def handle_message(data):
    message = data.get('message')
    sender_token = data.get('sender')

    # JWT 토큰이 존재하는지 먼저 확인
    if not sender_token:
        return {'error': '토큰이 제공되지 않았습니다.'}

    # JWT 토큰을 디코딩하여 사용자 이름을 가져옴
    try:
        if len(sender_token.split('.')) != 3:
            return {'error': '유효하지 않은 JWT 토큰 형식입니다.'}

        decoded = jwt.decode(sender_token, app.config['SECRET_KEY'], algorithms=['HS256'])
        sender = decoded['username']
    except jwt.ExpiredSignatureError:
        return {'error': '토큰이 만료되었습니다.'}
    except jwt.DecodeError:
        return {'error': '유효하지 않은 토큰입니다.'}

    print(f'Received message from {sender}: {message}')
    
    # 클라이언트에 메시지 전송 (sender 정보 포함)
    send({'message': message, 'sender': sender}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)  # Flask-SocketIO 서버 실행
