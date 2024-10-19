    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('recommendation-form');
        const badges = document.querySelectorAll('.badge');
        const selectedCategoriesInput = document.getElementById('selected_categories');

        // 뱃지 선택 이벤트 처리
        badges.forEach(badge => {
            badge.addEventListener('click', function() {
                this.classList.toggle('selected');
                const selectedCategories = Array.from(badges)
                    .filter(badge => badge.classList.contains('selected'))
                    .map(badge => badge.dataset.value);
                selectedCategoriesInput.value = selectedCategories.join(',');
            });
        });

        // 폼 제출 시 데이터 전송 및 결과 페이지로 이동
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(form);
            const data = {
                riot_tier: formData.get('riot_tier'),
                riot_position: formData.get('riot_position'),
                selected_categories: formData.get('selected_categories'),
                user_preference: formData.get('user_preference')  // content 대신 user_preference 사용
            };

            fetch('/api/profile/recommendation/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify(data),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // 결과 데이터를 /matching_result/ 페이지로 전달
                window.location.href = `/matching_result/?result=${encodeURIComponent(JSON.stringify(data))}`;
            })
            .catch(error => {
                console.error('Error:', error);
                alert("유저 추천 과정에서 오류가 발생했습니다. 다시 시도해 주세요.");
            });
        });
    });

    // CSRF 토큰 함수
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