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

<br>

## 📖 Navigation

1. [Introduction](#introduction)
2. [Setup](#setup)
3. [Features](#features)
4. [Techstack](#techstack)
5. [Architecture](#architecture)
6. [ERD](#erd)
7. [Team](#team)

<br>

<a name="introduction"></a>
## 👀 Introduction
![브로셔_v4](https://github.com/user-attachments/assets/e2a7b6d3-26fc-4137-a586-b67559eae9b4)


WP.GG는 리그 오브 레전드 유저들의 리뷰와 매칭 시스템을 통해, 긍정적인 팀 문화를 구축하고 즐거운 게임 경험을 만들어가는 공간입니다.

You can access the live demo of the project [here](wpgg.kr).


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
    POSTGRES_NAME = 'your_postgres_name_here'
    POSTGRES_USER = 'your_postgres_user_here'
    POSTGRES_PASSWORD = 'your_postgres_password_here'
    POSTGRES_HOST = 'your_postgre_host_here'

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

> * Riot과 Discord를 통한 간편 로그인을 지원합니다. (Riot Client Secret 발급 문제로 라이엇 계정 로그인 관련 기능은 추후에 추가 예정.)
> * 마이페이지에서 연결된 앱을 확인 할 수 있으며, 연결 해제도 가능합니다.
> * 연동된 라이엇 계정을 통한 라이엇 유저 정보(유저네임, 이메일, 프로필 사진, 선호 챔피언, 티어 등)를 불러옵니다.
<!-- > * 앱 당 하나의 계정만 연결 가능합니다. -->

<details>
<summary>미리보기</summary>
<div markdown="1">
    
<img width="1300" alt="스크린샷 2024-10-19 오전 3 00 52" src="https://github.com/user-attachments/assets/f9e09313-6775-4128-b7b3-dbfddbb530b3">
<img width="1300" alt="스크린샷 2024-10-19 오전 3 01 31" src="https://github.com/user-attachments/assets/5221a6e1-b98c-4e1c-9bd9-08ecba3e90ee">
<img width="1300" alt="스크린샷 2024-10-19 오전 3 02 36" src="https://github.com/user-attachments/assets/306b5c1a-67af-47ae-bf6e-dbeec3184ae5">

 <br>
</div>
</details>

<br>

### 👬 AI를 통한 유저 추천 기능
 
> * 포지션, 랭크 티어 기준을 선택하여 기준을 충족하는 유저만 추천받을 수 있습니다.
> * 평가 항목을 선택하여 해당 평가를 많이 받은 유저 위주로 추천받을 수 있습니다.
> * LLM이 유저들에 대한 리뷰 데이터를 수집합니다. 
> * 사용자가 선호하는 특징을 입력하면, AI가 사용자가 원하는 특징과 가장 부합하는 평가를 가진 유저와 매칭해줍니다.
> * 유저들이 많이 검색한 항목은 선택 항목에 자동으로 추가됩니다. (2024년 11월 업데이트 예정)

<details>
<summary>미리보기</summary>
<div markdown="1">

<img width="1300" alt="스크린샷 2024-10-19 오전 3 04 24" src="https://github.com/user-attachments/assets/2c21db92-2d8f-4569-9f1b-dab62144ec29">
<img width="1300" alt="스크린샷 2024-10-19 오전 3 05 30" src="https://github.com/user-attachments/assets/2294da29-9510-4ba8-8ad2-d38c50137c4a">

 <br>
</div>
</details>

<br>

### 💬 Polling 방식을 활용한 실시간 채팅

> * 실시간 채팅이 가능합니다.
> * 최근에 대화가 이루어진 순서대로 채팅방이 보여집니다.
> * 채팅 내역이 기록되며 이전에 한 채팅을 볼 수 있습니다.
> * 각 채팅은 채팅방 별로 구분됩니다.
<!-- > * 일대일 채팅과 그룹 채팅이 존재합니다. -->

<details>
<summary>미리보기</summary>
<div markdown="1">

<img width="1300" alt="스크린샷 2024-10-19 오전 3 21 06" src="https://github.com/user-attachments/assets/aa45630b-6ea0-410f-ba36-846bc610fe0e">

 <br>
</div>
</details>

<br>

### 🔍 라이엇 API와 연동한 유저 상세 정보 조회 기능

> * 유저 네임과 라이엇 태그를 함께 검색하면, 내 회원 상세 정보가 조회됩니다.
> * 라이엇 API와 연동되어, 리그오브레전드 프로필 아이콘, 유저 레벨, 솔로랭크 티어, 최근 전적, TOP 5 선호 챔피언 등의 라이엇 실시간 정보를 불러옵니다.
> * 라이엇 최근 매치 기록 정보를 바탕으로 현재 선호 포지션 정보도 제공합니다.
> * 검색된 유저의 평과 점수와, 해당 유저에 대한 리뷰글 목록이 출력됩니다.
> * 각 리뷰글을 클릭하면 리뷰 상세 조회가 가능합니다.

<details>
<summary>미리보기</summary>
<div markdown="1">

<img width="1300" alt="스크린샷 2024-10-19 오전 3 10 10" src="https://github.com/user-attachments/assets/5eb98c4b-949f-423a-91f5-2785f461713a">
<img width="1300" alt="스크린샷 2024-10-19 오전 3 09 23" src="https://github.com/user-attachments/assets/176cc292-7bc5-4a14-af58-d6672fe9bbc8">

 <br>
</div>
</details>

<br>

### ⚖️ 유저 평가 기능

> * 리뷰 대상이 될 유저를 검색하여 해당 유저에 대한 리뷰를 작성합니다.
> * 이모티콘을 선택해, 유저의 WP rating(Well Played Rating)를 평가합니다.
> * 평가 항목을 선택하여 유저의 평판에 영향을 줍니다.
> * 리뷰에 한 개 이상의 이미지를 업로드할 수 있습니다.
> * 다른 리뷰를 조회할 수 있습니다.
> * 리뷰 작성과 댓글 작성은 로그인한 상태에서만 가능합니다.

<details>
<summary>미리보기</summary>
<div markdown="1">
    
<img width="1300" alt="스크린샷 2024-10-19 오전 3 35 37" src="https://github.com/user-attachments/assets/91a666b5-eb12-4653-b72b-6bce951681f4">
<img width="1421" alt="스크린샷 2024-10-21 오후 3 39 40" src="https://github.com/user-attachments/assets/9baaac94-5d28-4961-a622-74f817468137">
<img width="1300" alt="스크린샷 2024-10-19 오전 3 46 02" src="https://github.com/user-attachments/assets/1db705e9-ede0-422c-aba7-f14ba465406f">
<img width="1300" alt="스크린샷 2024-10-19 오전 3 46 22" src="https://github.com/user-attachments/assets/656d3372-e153-4957-96ca-da4649e37c6d">

<br>
</div>
</details>

<br>

### 👥 팀 찾기 기능

> * 리그오브레전드를 같이 플레이할 팀을 생성할 수 있습니다.
> * 일반 모드(5명), 내전 모드(10명) 두가지 중 하나를 선택하여 생성할 수 있습니다.
> * 팀 생성 시에는 리그오브레전드 랭크, 서버를 선택합니다.
> * 파티원들의 나이, 성별, 사용 언어, 방장의 포지션을 입력한 정보를 기준으로 팀이 생성됩니다.
> * 유저는 원하는 파티에 조인하여 같이 게임을 할 유저를 찾을 수 있습니다.
> * 파티에서 더이상 소속되고 싶지않을 경우 나의 파티를 나갈 수 있습니다.

<details>
<summary>미리보기</summary>
<div markdown="1">

<img width="1440" alt="스크린샷 2024-10-21 오후 3 39 08" src="https://github.com/user-attachments/assets/e854e399-aec4-4b3c-9472-087ba3c149ae">

<br>
</div>
</details>

<br>


### 🎖 매너 랭킹 조회 기능

> * 우수한 평가 점수를 가진 순서로, 유저 순위가 공개됩니다.
> * 포지션을 필터링 하여 순위를 조회할 수 있습니다.
> * 랭킹 기준을 선택하여, 특정 평가 항목 기준으로도 순위를 조회할 수 있습니다.

<details>
<summary>미리보기</summary>
<div markdown="1">

<img width="1300" alt="스크린샷 2024-10-19 오전 3 14 31" src="https://github.com/user-attachments/assets/a2f4aff2-a5a3-41c3-a1d6-b6accb88076c">

<br>
</div>
</details>

<br>

### 👩🏻‍💻 마이 페이지 기능

> * 마이 페이지에서 내 정보 조회가 가능합니다.
> * 내 WP rating(평판 점수)와 소셜 계정 연결 여부를 확인할 수 있습니다.
> * 프로필 사진을 지정할 수 있습니다.
> * 프로필 사진이 없는 유저는 리그오브레전드 계정이 연결된 경우, 리그오브레전드 프로필 아이콘이 프로필 이미지로 지정됩니다.
> * 소셜 계정에 연결/해제 할 수 있습니다. (2024년 11월 13일 업데이트 예정)

<details>
<summary>미리보기</summary>
<div markdown="1">
    
<img width="1300" alt="스크린샷 2024-10-19 오전 3 43 07" src="https://github.com/user-attachments/assets/2a782d94-def0-4449-889a-dc6b2597831f">
<img width="1300" alt="스크린샷 2024-10-19 오전 3 43 27" src="https://github.com/user-attachments/assets/8ab6fd39-6325-42d2-885d-eb0bb3b88926">

<br>
</div>
</details>

<br>

### 🔔 실시간 알림 (2024년 11월 중순 업데이트 예정)

> * 실시간 채팅이 오면 실시간 알림을 제공하며 알림을 클릭하면 해당 채팅방으로 이동합니다.
> * 안읽은 알림 개수 만큼 화면에 표시됩니다.
> * 안읽은 알림이 50개 이상인 경우엔 50+개로 표시됩니다.
> * 안읽은 알림을 클릭하면 읽음 표시됩니다.
> * 모두 읽음 처리 기능 제공합니다.

<details>
<summary>미리보기</summary>
<div markdown="1">
  
<img width="780" alt="스크린샷 2024-10-08 오전 3 35 45" src="https://github.com/user-attachments/assets/cc4c3e50-eaa3-4814-be71-502d383b90bf">
<img width="360" alt="스크린샷 2024-10-08 오전 3 34 39" src="https://github.com/user-attachments/assets/a820a585-b20b-48df-be5a-189f115ab235">

 <br>
</div>
</details>

<br>

### 📢 신고 기능 (2024년 11월 중순 업데이트 예정)
 
> * 유저는 채팅 내용에 부적절한 내용이 있을 경우, 해당 채팅을 신고할 수 있습니다.
> * 금지어를 채팅에서 입력한 유저는 주의 대상으로 분류되어 일정 시간동안 채팅이 AI의 검수를 받고 필터링 되어 출력됩니다.
> * 본인은 본인을 신고할 수 없으며 같은 건의 신고에 대해서는 계정 하나당 1회로 제한됩니다.
> * 신고가 들어오면 관리자가 확인하게 되며, 관리자의 검수 후 패널티 대상으로 분류된 유저는 일정 시간동안 계정 사용이 금지됩니다.

<details>
<summary>미리보기</summary>
<div markdown="1">

<img width="400" alt="스크린샷 2024-10-08 오전 3 55 50" src="https://github.com/user-attachments/assets/37d89bc4-2983-462c-bde4-7c2d9caae353">
<img width="668" alt="스크린샷 2024-10-08 오전 3 52 31" src="https://github.com/user-attachments/assets/14ce05e7-1d0b-4ba0-81fe-a0f9d1f5a83b">

 <br>
</div>
</details>

<br>

### 💸 크레딧 기능 (2024년 12월 업데이트 예정)
 
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
## 📝 Technologies & Tools
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white"> <img src="https://img.shields.io/badge/DRF-092E20?style=for-the-badge&logo=Django&logoColor=white"> <img src="https://img.shields.io/badge/DRF SimpleJWT-092E20?style=for-the-badge&logo=Django&logoColor=white"> <img src="https://img.shields.io/badge/django--allauth-092E20?style=for-the-badge&logo=Django&logoColor=white"> <img src="https://img.shields.io/badge/django--cors--headers-092E20?style=for-the-badge&logo=Django&logoColor=white"> <img src="https://img.shields.io/badge/Requests-3776AB?style=for-the-badge&logo=Python&logoColor=white"> <img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=PostgreSQL&logoColor=white"> <img src="https://img.shields.io/badge/AWS EC2-FF9900?style=for-the-badge&logo=Amazon-AWS&logoColor=white"> <img src="https://img.shields.io/badge/AWS RDS-527FFF?style=for-the-badge&logo=Amazon-RDS&logoColor=white"> <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=Redis&logoColor=white"> <img src="https://img.shields.io/badge/OpenAI API-412991?style=for-the-badge&logo=OpenAI&logoColor=white"> <img src="https://img.shields.io/badge/Riot API-D32936?style=for-the-badge&logo=Riot-Games&logoColor=white"> <img src="https://img.shields.io/badge/Discord API-5865F2?style=for-the-badge&logo=Discord&logoColor=white"> <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=white"> <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=HTML5&logoColor=white"> <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=CSS3&logoColor=white"> <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=NGINX&logoColor=white"> <img src="https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=Gunicorn&logoColor=white"> <img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=Ubuntu&logoColor=white"> <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white"> <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white"> <img src="https://img.shields.io/badge/Visual Studio Code-007ACC?style=for-the-badge&logo=Visual-Studio-Code&logoColor=white"> <img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white"> <img src="https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=Notion&logoColor=white"> <img src="https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=Slack&logoColor=white"> <img src="https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=Figma&logoColor=white"> <img src="https://img.shields.io/badge/Zep-4A154B?style=for-the-badge&logo=Zep&logoColor=FFFFFF">


<br>

<a name="architecture"></a>
## 🌐 Architecture
<img width="900" alt="스크린샷 2024-10-19 오후 10 02 16" src="https://github.com/user-attachments/assets/4297834c-b82a-488e-99b0-60fb97cb6beb">

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
#### [🌟 프로젝트 브로셔 보러가기](https://www.notion.so/teamsparta/WP-GG-10c2dc3ef514808db154fa056e53559b)

