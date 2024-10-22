function deletemethod(itemId) {
    console.log('삭제할 itemId:', itemId);  // itemId를 콘솔에 출력

    const url = `http://127.0.0.1:8000/api/party/${itemId}`; // 엔드포인트에 변수를 포함한 URL

    fetch(url, {
        method: 'DELETE',
    })
        .then(response => {
            if (response.ok) {
                alert('삭제 성공');
            } else {
                alert('삭제 실패');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
};

function getAccessToken() {
    return localStorage.getItem('access_token');
}

// document.getElementById("createparty").addEventListener('submit', function(e) {
//     e.preventDefault();
//     const formData2 = new FormData(document.getElementById("createparty"));

//     const rank = new formData2(document.getElementById("rank"));
//     const server = new formData2(document.getElementById("server"));
//     const gender = new formData2(document.getElementById("gender"));
//     const age = new formData2(document.getElementById("age"));
//     const language = new formData2(document.getElementById("language"));
//     const position = new formData2(document.getElementById("position"));
//     const is_rank = new formData2(document.getElementById("is_rank"));


//     console.log("a")
//     url = 'http://127.0.0.1:8000/api/party/';
//     fetch(url, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': '{{ csrf_token }}', 'Authorization': 'Bearer ' + getAccessToken() // CSRF 토큰을 헤더에 포함
//         },
//         body: formData2
//     })
//         .then(response => {
//             if (response.ok) {
//                 alert('삭제 성공');
//             } else {
//                 alert('삭제 실패');
//             }
//         })
//         .catch(error => {
//             console.error('Error:', error);
//         });
// });

document.getElementById('createparty').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const jsonData = {};
    formData.forEach((value, key) => {
        jsonData[key] = value;
    });

    fetch('http://127.0.0.1:8000/api/party/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}', 'Authorization': 'Bearer ' + getAccessToken() // CSRF 토큰 추가
        },
        body: JSON.stringify(jsonData)
    })
    .then(response => {
        response_json = response.json()
        console.log(response_json);
        if response_json.data = "error"{
            alert('실패')
        }
        else{
            alert('성공')
        }

    })
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
});



function positionprint() {
    console.log('console print');
}

function consoleprint(action) {
    console.log(action);
}