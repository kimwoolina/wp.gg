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
    // fetch('/parties/' + itemId + '/', {
    //     method: 'DELETE',
    //     headers: {
    //         'X-CSRFToken': csrftoken,
    //     },
    // })
    // .then(response => response.json())
};

function positionprint() {
    console.log('console print');
}

function consoleprint(action) {
    console.log(action);
}