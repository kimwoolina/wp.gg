

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
    console.log("headers:", headers)

    fetch('/api/party/', {
        method: 'DELETE',
        headers: headers,
        body: JSON.stringify({ id: partyId })
    })
    .then(response => {
        if (response.ok) {
            alert("파티가 삭제되었습니다.");
        } else {
            alert("삭제 실패: " + response.statusText);
        }
    })
    .then(data => {
        console.log(data);
        location.reload(); // 화면 새로고침
    })
    .catch(error => console.error('Error:', error));
}


function JoinParty(partyId, position) {
    console.log(partyId);
    console.log(position);
    const url = `/api/party/${partyId}/`; // 엔드포인트에 변수를 포함한 URL
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
        'Authorization': 'Bearer ' + getAccessToken()
    }
    console.log("headers:", headers)

    fetch(url, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({ position:position })
    })
    .then(response => {
        if (response.ok) {
            alert("파티에 참여하였습니다.");
        } else {
            alert("참여 실패: " + response.statusText);
        }
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
    console.log("headers:", headers)

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


function positionprint(position) {
    console.log(position);
}

function consoleprint(action) {
    console.log(action);
}