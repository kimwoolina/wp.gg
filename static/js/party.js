

function getAccessToken() {
    return localStorage.getItem('access_token');
}


document.getElementById('createparty').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const jsonData = {};
    formData.forEach((value, key) => {
        jsonData[key] = value;
    });
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/api/party/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{csrftoken}}',
            'Authorization': 'Bearer ' + getAccessToken()
        },
        body: JSON.stringify(jsonData)
    })
    .then(response => {
        if (!response.ok) {
            console.log(response)
            throw new Error('Network response was not ok');
        }
        return response.json(); // 응답을 JSON 형식으로 변환
    })
    .then(data => {
        console.log(data);
        location.reload(); // 화면 새로고침
    })
    .catch(error => console.error('Error:', error));
});



function deleteparty(partyId) {

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': '{{csrftoken}}',
        'Authorization': 'Bearer ' + getAccessToken()
    }

    fetch('/api/party/', {
        method: 'DELETE',
        headers: headers,
        body: JSON.stringify({ id: partyId, status:'Forced deletion' })
    })
    .then(response => {
        if (response.ok) {
            alert("파티가 삭제되었습니다.");
            return response.json(); // 응답 데이터가 있으면 처리
        } else {
            return response.json().then(data => { 
                // 서버에서 받은 에러 메시지를 출력
                alert("삭제 실패: " + (data.detail || response.statusText)); 
                // throw new Error(data.detail || response.statusText);
            });
        }
    })
    .then(data => {
        location.reload(); // 화면 새로고침
    })
    // .catch(error => console.error('Error:', error));
}


// function deleteparty(partyId) {

//     const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
//     const headers = {
//         'Content-Type': 'application/json',
//         'X-CSRFToken': csrftoken,
//         'Authorization': 'Bearer ' + getAccessToken()
//     };

//     // 삭제 요청을 보내는 함수
//     function sendDeleteRequest(status = 'deletion') {
//         fetch('/api/party/', {
//             method: 'DELETE',
//             headers: headers,
//             body: JSON.stringify({ id: partyId, status: status })
//         })
//         .then(response => {
//             return response.json().then(data => {
//                 if (response.ok) {
//                     alert("파티가 삭제되었습니다.");
//                     location.reload();  // 성공 시에만 새로고침
//                 } else {
//                     alert("삭제 실패: " + data.message); // 서버에서 받은 에러 메시지를 출력
//                     showModal(); // 실패 시 모달 표시
//                 }
//             });
//         })
//         // .catch(error => {
//         //     console.error('Error:', error);
//         //     showModal(); // 오류 발생 시 모달 표시
//         // });
//     }

//     // 모달 표시 함수
//     function showModal() {
//         const modal = document.getElementById('errorModal');
//         modal.style.display = 'block'; // 모달을 표시
//     }

//     // 모달의 다시 시도 버튼에 이벤트 추가
//     document.getElementById('retryButton').addEventListener('click', function(event) {
//         // event.preventDefault(); // 기본 동작 중단
//         // document.getElementById('errorModal').style.display = 'none'; // 모달 닫기
//         // sendDeleteRequest('Forced deletion'); // status를 'Forced deletion'으로 변경하여 다시 요청
//     });

//     sendDeleteRequest(); // 처음 요청을 보냄
// }



function JoinParty(partyId, position) {
    const url = `/api/party/${partyId}/`; // 엔드포인트에 변수를 포함한 URL
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
        'Authorization': 'Bearer ' + getAccessToken()
    }

    fetch(url, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({ position:position })
    })
    .then(response => {
        return response.json().then(data => {
            if (response.ok) {
                alert("파티에 참여하였습니다.");
            } else {
                alert("참여 실패: " + data.message); // 서버에서 받은 에러 메시지를 출력
                throw new Error(data.message);
            }
        });
    })
    .then(data => {
        console.log(data);
        location.reload(); // 화면 새로고침
    })
    .catch(error => console.error('Error:', error));
}


function GetOutParty(partyId) {
    console.log(partyId);
    console.log(position);
    const url = `/api/party/${partyId}/`; // 엔드포인트에 변수를 포함한 URL
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
        'Authorization': 'Bearer ' + getAccessToken()
    }

    fetch(url, {
        method: 'DELETE',
        headers: headers,
    })
    .then(response => {
        if (response.ok) {
            alert("파티에서 탈퇴하였습니다.");
        } else {
            alert("탈퇴 실패: " + response.statusText);
        }
    })
    .then(data => {
        console.log(data);
        location.reload(); // 화면 새로고침
    })
    .catch(error => console.error('Error:', error));
}


const currentUser = "{{ request.user }}"; // 또는 다른 사용자 속성



function GetPosition(party) {
    if (party.top1 == currentUser) {
        return "top1";
    } else if (party.mid1 == currentUser) {
        return "mid1";
    } else if (party.jungle1 == currentUser) {
        return "jungle1";
    } else if (party.adc1 == currentUser) {
        return "adc1";
    } else if (party.support1 == currentUser) {
        return "support1";
    }
    if (party.is_rank){
        if (party.top2 == currentUser) {
            return "top2";
        } else if (party.mid2 == currentUser) {
            return "mid2";
        } else if (party.jungle2 == currentUser) {
            return "jungle2";
        } else if (party.adc2 == currentUser) {
            return "adc2";
        } else if (party.support2 == currentUser) {
            return "support2";
        }
    }

}


// 드롭다운 js
function toggleDropdown(event) {
    const dropdownMenu = document.getElementById("dropdownMenu");
    dropdownMenu.style.display = dropdownMenu.style.display === "block" ? "none" : "block"; // 토글
    event.stopPropagation(); // 클릭 이벤트가 문서에 전파되지 않도록 함
}

// 문서의 다른 부분 클릭 시 드롭다운 메뉴 닫기
document.addEventListener("click", function() {
    const dropdownMenu = document.getElementById("dropdownMenu");
    if (dropdownMenu != null) {
        dropdownMenu.style.display = "none"; // 숨김
    }
});


function consoleprint(action) {
    alert("준비중인 서비스입니다.")
}

function click_user_img(user_pk) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
        'Authorization': 'Bearer ' + getAccessToken()
    }

    fetch(`/${user_pk}/`, {
        method: 'DELETE',
        headers: headers,
    })
    .then(response => {
        if (response.ok) {
            alert("파티에서 탈퇴하였습니다.");
        } else {
            alert("탈퇴 실패: " + response.statusText);
        }
    })
    .then(data => {
        console.log(data);
        location.reload(); // 화면 새로고침
    })
    .catch(error => console.error('Error:', error));
}