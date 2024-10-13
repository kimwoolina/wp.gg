// 로그인 처리
document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'email': email,
            'password': password,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            alert('로그인 성공!');
            // 로그인 후 필요한 행동들 작성
        } else {
            alert('로그인 실패: ' + data.error);
        }
    })
    .catch(error => console.error('로그인 중 오류 발생:', error));
});

// 회원가입 처리
document.getElementById('signupForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/signup/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'email': email,
            'username': username,
            'password': password,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('회원가입 성공!');
            // 회원가입 후 필요한 행동들 작성
        } else {
            alert('회원가입 실패: ' + data.error);
        }
    })
    .catch(error => console.error('회원가입 중 오류 발생:', error));
});
