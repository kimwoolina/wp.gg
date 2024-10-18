![header](https://capsule-render.vercel.app/api?type=wave&height=300&color=gradient&text=wp.gg)

[![Python Version](https://img.shields.io/badge/Python-3.10-3776AB)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/Django-4.2-092E20)](https://www.djangoproject.com/)
[![DRF Version](https://img.shields.io/badge/Django_Rest_Framework-3.15.2-ff1709)](https://www.django-rest-framework.org/)
[![Channels](https://img.shields.io/badge/Channels-4.1.0-2C8EBB)](https://channels.readthedocs.io/)
[![channels-redis](https://img.shields.io/badge/channels--redis-4.2.0-DC382D)](https://channels.readthedocs.io/en/stable/)
[![django-allauth](https://img.shields.io/badge/django--allauth-65.0.2-306998)](https://django-allauth.readthedocs.io/)
[![dj-rest-auth](https://img.shields.io/badge/dj--rest--auth-6.0.0-0F4C81)](https://dj-rest-auth.readthedocs.io/)
[![djangorestframework-simplejwt](https://img.shields.io/badge/djangorestframework--simplejwt-5.3.1-092E20)](https://django-rest-framework-simplejwt.readthedocs.io/)
[![Requests](https://img.shields.io/badge/Requests-2.32.3-FF5B5B)](https://requests.readthedocs.io/)
[![Redis](https://img.shields.io/badge/Redis-5.1.0-dc382d)](https://redis.io/)
[![OpenAI Python Client](https://img.shields.io/badge/OpenAI%20Python%20Client-0.28.0-4B92DB)](https://github.com/openai/openai-python)
[![RIOT API](https://img.shields.io/badge/RIOT_API-red)](https://developer.riotgames.com/)
[![Discord API](https://img.shields.io/badge/Discord_API-7289da)](https://discord.com/developers/docs/intro)

<br>

## 📖 Navigation

1. [Introduction](#introduction)
2. [Setup](#setup)
3. [핵심기능](#features)
4. [적용기술](#techstack)
5. [Architecture](#architecture)
6. [ERD](#erd)
7. [Team](#team)

<br>

<a name="introduction"></a>
## 👀 Introduction
![브로셔_v4](https://github.com/user-attachments/assets/e2a7b6d3-26fc-4137-a586-b67559eae9b4)


WP.GG는 리그 오브 레전드 유저들의 리뷰와 매칭 시스템을 통해, 긍정적인 팀 문화를 구축하고 즐거운 게임 경험을 만들어가는 공간입니다.

### 🗓 Duration
24.09.30  ~ing

<br>

<a name="setup"></a>
## 🛠 Setup 
To set up and run the project, follow these steps:

1. Clone the project repository:

    ```bash
    git clone https://github.com/kimwoolina/wp.gg.git
    ```

2. Navigate to the project directory:

    ```bash
    cd /Users/YourPC/Your_Cloned_Folder/
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create and configure the `config.py` file:**

    Create a file named `config.py` in the project root directory and add the following content:

    ```python
    # config.py

    DJANGO_SECRET_KEY = "your_django_secret_key_here"
    RIOT_API_KEY = "your_riot_api_key_here"
    OPENAI_API_KEY = "your_openai_api_key_here"
    DISCORD_CLIENT_ID = 'your_discord_client_id_here'
    DISCORD_SECRET_ID = 'your_discord_secret_id_here'
    DISCORD_OAUTH2_URL = 'your_discord_oauth2_url_here'

    ```

5. **Apply database migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

7. **Open your browser and visit:**

    [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
<br><br><br>

<a name="features"></a>
## 핵심 기능
### 🛡 OAuth2 소셜로그인 (Riot, Discord)

> * Riot과 Discord를 통한 간편 로그인을 구현 예정입니다. (Riot Client Secret 발급 문제로 라이엇 계정 로그인 관련 기능은 1차 배포 후에 추가 예정.)
> * 앱 당 하나의 계정만 연결 가능합니다.
> * 마이페이지에서 연결된 앱을 확인 할 수 있으며, 연결 해제도 가능합니다.
> * 연동된 라이엇 계정을 통한 라이엇 유저 정보(선호 챔피언, 티어 등)를 불러옵니다.

<details>
<summary>미리보기</summary>
<div markdown="1">

<img width="900" alt="스크린샷 2024-10-08 오전 3 30 16" src="https://github.com/user-attachments/assets/833bbeef-ed4a-44df-9a31-d82adaf7707a">

<img width="900" alt="스크린샷 2024-10-11 오전 12 32 13" src="https://github.com/user-attachments/assets/08cd662a-e004-4d50-9798-e35f5805eed3">


 <br>
</div>
</details>

<br>

### 👬 AI를 통한 유저 추천 기능
 
> * LLM을 활용하여 유저들에 대한 리뷰 데이터를 수집합니다.
> * 사용자가 선호하는 특징과 가장 부합하는 평가를 가진 유저와 매칭해줍니다.
> * 유저들이 많이 검색한 항목은 선택 항목에 자동으로 추가됩니다.

<details>
<summary>미리보기</summary>
<div markdown="1">

<img width="674" alt="스크린샷 2024-10-08 오전 3 49 01" src="https://github.com/user-attachments/assets/97eced44-665d-4bff-a383-1daabede709c">

 <br>
</div>
</details>

<br>

### 💬 WebSocket을 활용한 실시간 채팅

> * 실시간 채팅이 가능합니다.
> * 최근에 대화가 이루어진 순서대로 채팅방이 보여집니다.
> * 채팅 내역이 기록되며 이전에 한 채팅을 볼 수 있습니다.
> * 각 채팅은 채팅방 별로 구분됩니다.
> * 일대일 채팅과 그룹 채팅이 존재합니다.

<details>
<summary>미리보기</summary>
<div markdown="1">

<img width="750" alt="스크린샷 2024-10-08 오전 3 54 58" src="https://github.com/user-attachments/assets/f896cfb8-a758-4dbc-a74d-05125e6d464e">

 <br>
</div>
</details>

<br>

### 🔔 실시간 알림

> * 실시간 채팅이 오면 실시간 알림을 제공하며 알림을 클릭하면 해당 채팅방으로 이동합니다.
> * 안읽은 알림 개수 만큼 화면에 표시됩니다.
> * 안읽은 알림이 50개 이상인 경우엔 50+개로 표시됩니다.
> * 안읽은 알림을 클릭하면 읽음 표시됩니다.
> * 모두 읽음 처리 기능 제공합니다.

<details>
<summary>미리보기</summary>
<div markdown="1">
  
<img width="783" alt="스크린샷 2024-10-08 오전 3 35 45" src="https://github.com/user-attachments/assets/cc4c3e50-eaa3-4814-be71-502d383b90bf">

<img width="363" alt="스크린샷 2024-10-08 오전 3 34 39" src="https://github.com/user-attachments/assets/a820a585-b20b-48df-be5a-189f115ab235">

 <br>
</div>
</details>

<br>

### 📢 신고 기능 
 
> * 유저는 채팅 내용에 부적절한 내용이 있을 경우, 해당 채팅을 신고할 수 있습니다.
> * 금지어를 채팅에서 입력한 유저는 주의 대상으로 분류되어 일정 시간동안 채팅이 AI의 검수를 받고 필터링 되어 출력됩니다.
> * 본인은 본인을 신고할 수 없으며 같은 건의 신고에 대해서는 계정 하나당 1회로 제한됩니다.
> * 신고가 들어오면 관리자가 확인하게 되며, 관리자의 검수 후 패널티 대상으로 분류된 유저는 일정 시간동안 계정 사용이 금지됩니다.

<details>
<summary>미리보기</summary>
<div markdown="1">

<img width="392" alt="스크린샷 2024-10-08 오전 3 55 50" src="https://github.com/user-attachments/assets/37d89bc4-2983-462c-bde4-7c2d9caae353">

<img width="668" alt="스크린샷 2024-10-08 오전 3 52 31" src="https://github.com/user-attachments/assets/14ce05e7-1d0b-4ba0-81fe-a0f9d1f5a83b">

 <br>
</div>
</details>

<br>

### 💸 크레딧 기능
 
> * 유저는 하루에 5개까지의 유저 상세 리뷰를 크레딧 차감 없이 조회할 수 있습니다.
> * 하루에 6번째 리뷰부터는 한개의 리뷰당 50개의 크레딧이 차감됩니다. 
> * 한번 조회한 리뷰는 하루동안 무제한으로 크레딧 차감없이 조회할 수 있습니다.
> * 크레딧 추가 결제가 필요한 경우, 광고를 보면 크레딧을 얻을 수 있게합니다.

<details>
<summary>미리보기</summary>
<div markdown="1">
    
<img width="647" alt="스크린샷 2024-10-08 오전 4 02 30" src="https://github.com/user-attachments/assets/f14efd5f-3907-4c73-9f9c-96b23f9cd613">

 <br>
</div>
</details>

<br><br>

<a name="techstack"></a>

<a name="architecture"></a>
## 🌐 Architecture
![image](https://github.com/user-attachments/assets/7117e8ac-c231-4403-8023-57de20cbf2cf)

<br>

<a name="erd"></a>
## 🗂 ERD
<img width="822" alt="스크린샷 2024-10-08 오후 12 56 04" src="https://github.com/user-attachments/assets/168bb3a7-d400-4570-813e-f64298595284">

<br><br>

<a name="team"></a>
## 👨‍👩‍👧‍👦 Team

| **Name**         | **GitHub Handle**                          | **Responsibilities**                                                                                           |
|------------------|------------------------------------------------|-------------------------------------------------------------------------------------------|
| **Woolin Kim**👑  | [@kimwoolina](https://github.com/kimwoolina)   | 소셜 로그인 연동, 라이엇 API 사용, 유저 추천 기능(LLM 활용), 채팅 기능, 유저 검색 기능 등 |
| **Saeye Lee**    | [@saeye](https://github.com/saeye)             | 회원가입, 로그인 등 인증 기능, 신고 관련 기능 , 비하발언 감지 기능(LLM), UI/UX 등 |
| **Nahee Kim**    | [@sptcnl](https://github.com/sptcnl)           | 리뷰, 댓글, 크레딧(결제) 관련 기능, UI/UX 등 |
| **Minseong Jeon**  | [@Oztalun](https://github.com/Oztalun)       | 배포, 파티 관련 기능 (팀 생성, 방장 교체, 팀원 내보내기, 팀 삭제 등) |

#### [📝 SA 문서 바로가기](https://www.notion.so/teamsparta/SA-97b05811e819459db6bfd1cd79ae6c1a)
#### [👊 팀 노션 바로가기](https://www.notion.so/teamsparta/fff2dc3ef5148112a832fd4cdd59b2c1)

