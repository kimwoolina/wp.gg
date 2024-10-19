    // Bearer 토큰 가져오는 함수
    function getAccessToken() {
        return localStorage.getItem('access_token');
    }

    // CSRF 토큰을 가져오는 함수
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    const csrftoken = getCookie('csrftoken');

    // 유저 검색 기능
    document.getElementById('search-icon').addEventListener('click', function() {
        const query = document.getElementById('user-search').value;
        const revieweeSelect = document.getElementById('reviewee');
        revieweeSelect.innerHTML = '<option value="">--평가 할 사람을 고르세요--</option>';

        fetch(`/api/articles/search_user/?q=${query}`, {
            method: 'GET', 
            headers: {
                'X-CSRFToken': csrftoken, 
                'Authorization': 'Bearer ' + getAccessToken() 
            }
            })
            .then(response => response.json())
            .then(data => {
                if (data.users.length === 0) {
                    return;
                }
                data.users.forEach(user => {
                    const option = document.createElement('option');
                    option.textContent = `${user.username} | ${user.riot_username || ''}${user.riot_tag || ''}`;
                    option.value = user.id;
                    revieweeSelect.appendChild(option);
                });
            });
    }
    );

    // 리뷰 카테고리 선택 기능
    document.addEventListener('DOMContentLoaded', function() {
        const badges = document.querySelectorAll('.badge');
        const selectedCategoriesInput = document.getElementById('selected_categories');
    
        badges.forEach(badge => {
            badge.addEventListener('click', function() {
                // 선택된 뱃지에 'selected' 클래스 추가/제거
                this.classList.toggle('selected');
    
                // 선택된 카테고리를 hidden input에 업데이트
                const selectedCategories = Array.from(badges)
                    .filter(badge => badge.classList.contains('selected'))
                    .map(badge => badge.dataset.category);
    
                // 원하는 형식으로 변환
                const categoryValues = {};
                badges.forEach(badge => {
                    const categoryName = badge.dataset.category;
                    if (badge.classList.contains('selected')){
                        categoryValues[categoryName] = 1
                    }
                });
    
                selectedCategoriesInput.value = JSON.stringify(categoryValues); // JSON 형태로 직렬화하여 저장
            });
        });
    });

    // 이미지 미리보기 기능
    function previewImages(event) {
        const previewContainer = document.getElementById('image-preview');
        previewContainer.innerHTML = '';

        const files = event.target.files;
        Array.from(files).forEach(file => {
            const reader = new FileReader();
            reader.onload = function (e) {
                const imgElement = document.createElement('img');
                imgElement.src = e.target.result;
                imgElement.style.maxWidth = '100px';
                imgElement.style.marginRight = '10px';
                previewContainer.appendChild(imgElement);
            };
            reader.readAsDataURL(file);
        });
    }


    // 리뷰 작성
    document.getElementById('articleForm').addEventListener('submit', function(event) {
        event.preventDefault();  // 폼의 기본 제출 동작 막기
    
        const revieweeSelect = document.getElementById('reviewee');
        if (revieweeSelect.value === "") {
            alert("평가 할 유저를 선택해주세요.");  // 경고 메시지 표시
            return;
        }
    
        // Bearer 토큰 가져오기
        const accessToken = getAccessToken();
    
        // 폼 데이터 가져오기
        const formData = new FormData(this);
    
        // fetch로 폼 데이터 전송
        fetch(this.action, {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + accessToken,  // Bearer 토큰 추가
                'X-CSRFToken': csrftoken
            },
            body: formData  // 폼 데이터 전송
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            window.location.href = '/article_list/';
        })
        .catch(error => {
            console.error('Error:', error);
            alert(data.message);
            window.location.href = '/article_list/';
        });
    });
