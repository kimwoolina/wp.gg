from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.registration.views import RegisterView
from django.contrib.auth import get_user_model, logout, update_session_auth_hash
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework import generics
from django.db.models import F, Q
from .models import Evaluations
from articles.models import Articles
from .serializers import UserSerializer, EvaluationSerializer, ArticleSerializer,  UserRankingSerializer, UserProfileSerializer
from .bots import ask_chatgpt
from django.db import models

from wpgg.settings import DiscordOAuth2
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
import requests
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_backends

from django.views.generic import TemplateView
from django.shortcuts import render


# 회원가입
class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        # 회원가입 완료시 메시지
        if response.status_code == status.HTTP_204_NO_CONTENT:
            response = Response({"message": "회원가입이 완료되었습니다😊"}, status=status.HTTP_201_CREATED)
        
        # if response.status_code == status.HTTP_201_CREATED:
        #     response.data['message'] = '회원가입이 완료되었습니다😊'
        
        return response

# 로그인
class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_200_OK:
            user = self.request.user
            username = user.username

            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response.data = {
                'message': f'{username}님 안녕하세요😊',
                'access': access_token,
                'refresh': refresh_token
            }
            
            # access_token, refresh_token 없으면 에러 메시지 
            if not access_token or not refresh_token:
                response.data['error'] = '토큰을 발급받지 못했습니다.'

        return response
    
# 로그아웃
class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        logout(request) 
        return Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)


# 회원탈퇴
User = get_user_model()

class CustomDeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]  

    def delete(self, request, *args, **kwargs):
        user = request.user  
        user.delete() # 유저 정보 아예 삭제할건지 팀원들과 이야기해봐야 함

        logout(request)

        return Response({"message": "회원탈퇴 완료! 그동안 이용해주셔서 감사했습니다👋"}, status=status.HTTP_200_OK)
    
    
# 마이페이지 조회 및 수정
class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]  

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 비밀번호 변경
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        form = PasswordChangeForm(user, request.data)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            return Response({"message": "비밀번호가 변경되었습니다."}, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.GenericAPIView):
    """
    유저를 검색하여 해당하는 유저의 상세정보 조회
    작성자: 김우린
    작성 날짜: 2024.09.30

    메서드:
        GET: 특정 사용자의 riot_username과 riot_tag에 따른 정보를 반환합니다.
    """
    
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        riot_tag = request.query_params.get('riot_tag')

        # riot_tag가 있으면 같이 필터링, 없으면 riot_username만 필터링
        filters = {'riot_username': username}
        if riot_tag:
            filters['riot_tag'] = riot_tag
        
        ''' 
        # test
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)  # 직렬화
        return Response(serializer.data)
        '''
        
        # 유저검색
        if riot_tag:
            user = User.objects.filter(**filters).first()
        else:
            # riot_tag가 없을 때 해당 유저네임으로 필터링
            user_queryset = User.objects.filter(riot_username=username)

            if user_queryset.exists():
                # 검색 결과가 있을 때
                if user_queryset.count() == 1:
                    # 유저가 한 명인 경우, 상세 정보 바로 조회
                    user = user_queryset.first()
                else:
                    # 유저가 여러 명인 경우, 필요한 필드만 가져오기
                    user_list = user_queryset.values('riot_username', 'riot_tag')
                    return Response({
                        "users": list(user_list)
                    })
            else:
                return Response({"message": f"{username} 소환사에 대한 정보를 찾을 수 없습니다."})
        
        
        if user:
            # reviewee로서 해당 사용자가 작성한 게시글 목록 가져오기
            articles = Articles.objects.filter(reviewee=user)
            serializer = self.get_serializer(user)
            serializer_data = serializer.data
            
            # Evaluations를 serializer_data에 추가
            try:
                evaluations = Evaluations.objects.get(user=user)
                serializer_data['evaluations'] = EvaluationSerializer(evaluations).data
            except Evaluations.DoesNotExist:
                serializer_data['evaluations'] = None
                
            # articles를 serializer_data에 추가
            article_serializer = ArticleSerializer(articles, many=True)
            serializer_data['articles'] = article_serializer.data
            
            return Response(serializer_data)

        return Response({"message": "해당 소환사에 대한 평판 정보가 없습니다."})


class MannerRankingView(ListAPIView):
    """
    유저 매너 랭킹 - 총점, 평가항목 순으로 정렬 기능, 포지션과 티어 필터 기능
    작성자: 김우린
    작성 날짜: 2024.10.01
    """
    
    serializer_class = UserRankingSerializer

    def list(self, request, *args, **kwargs):
        # 기본 정렬 기준은 'User.score'
        sort_by = self.request.query_params.get('sort_by', 'score')

        # 가능한 정렬 기준 필드를 딕셔너리로 정의 (Evaluations 필드 포함)
        sort_fields = {
            'score': 'score',
            'kindness': 'evaluations__kindness',
            'teamwork': 'evaluations__teamwork',
            'communication': 'evaluations__communication',
            'mental_strength': 'evaluations__mental_strength',
            'punctualiity': 'evaluations__punctualiity',
            'positivity': 'evaluations__positivity',
            'mvp': 'evaluations__mvp',
            'mechanical_skill': 'evaluations__mechanical_skill',
            'operation': 'evaluations__operation',
            'negativity': 'evaluations__negativity',
            'profanity': 'evaluations__profanity',
            'afk': 'evaluations__afk',
            'cheating': 'evaluations__cheating',
            'verbal_abuse': 'evaluations__verbal_abuse',
        }

        # 쿼리 매개변수에 따라 정렬 기준 설정, 없으면 'score'로 정렬
        sort_by_field = sort_fields.get(sort_by, 'score')

        # 포지션 필터링 처리
        positions = request.query_params.getlist('positions')  # 다중 포지션 가져오기
        # 리뷰가 존재하는 유저 정보만 가져오기
        queryset = User.objects.filter(evaluations__isnull=False).select_related('evaluations')

        # 여러 포지션으로 필터링
        if positions:
            position_query = Q()
            for position in positions:
                position_query |= Q(positions__position_name=position)  # OR 조건 추가
            queryset = queryset.filter(position_query)

        # 쿼리셋을 정렬
        queryset = queryset.order_by(F(sort_by_field).desc(nulls_last=True))

        # 쿼리셋이 비어 있을 경우 메시지와 빈 리스트를 반환
        if not queryset.exists():
            return Response({"message": "해당 조건에 맞는 유저 정보가 없습니다.", "users": []}, status=status.HTTP_200_OK)

        # 정상적인 결과가 있을 경우
        serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return render(request, 'users/rankings.html', {'users': serializer.data})

class RankingView(TemplateView):
    template_name = 'users/rankings.html' 
    
    
class UserRecommendationView(APIView):
    """
    티어, 포지션, 평가항목 선택하고 원하는 유저 상을 입력하여 유저 매칭해줌
    작성자: 김우린
    작성 날짜: 2024.10.09
    """

    def get(self, request, *args, **kwargs):
        # 초기화
        matching_reviewee_id = None

        # 요청에서 필터링 값 가져오기
        riot_tiers = request.GET.getlist('riot_tier', [])
        positions = request.GET.getlist('positions', [])
        filter_fields = request.GET.getlist('filter_fields', [])
        user_preference = request.GET.get('user_preference', '')

        # 기본 유저 리스트 가져오기
        users = User.objects.all()

        # 1. 기본 필터링 (티어와 포지션에 따라 필터링)
        if riot_tiers:
            users = users.filter(riot_tier__in=riot_tiers)

        if positions:
            users = users.filter(positions__position_name__in=positions)

        # 2. 평가 필드 필터링
        # if filter_fields:
        #     order_by_fields = [f'-evaluations__{field}' for field in filter_fields]
        #     users = users.order_by(*order_by_fields)
        if filter_fields:
            # 필터링 조건 추가
            filter_conditions = {}
            for field in filter_fields:
                if hasattr(Evaluations, field):
                    filter_conditions[f'evaluations__{field}__gte'] = 1  # 필드 값이 1 이상인 경우

            # 유저 필터링
            users = users.filter(**filter_conditions)

            # 평가 항목이 있는 유저만 필터링 후 정렬
            users = users.filter(evaluations__isnull=False).annotate(
                evaluations_count=models.Count('evaluations')
            ).order_by(*[f'-evaluations__{field}' for field in filter_fields]).distinct()

            # 상위 3명만 선택
            users = users[:3]

        # 리뷰 데이터 가져오기
        all_reviews = Articles.objects.all().values('content', 'reviewee')
        reviews_text = "\n".join([f"Review ID: {review['reviewee']} - {review['content']}" for review in all_reviews])

        # 3. 사용자 입력 텍스트 처리
        if user_preference:
            # OpenAI API를 사용하여 유저의 선호도에 맞는 리뷰 분석
            system_instructions = """
            You are tasked with finding the most relevant review for a user based on their preferences.
            Based on the user's preference, identify the review that best matches the following description: {user_preference}.
            Here are all the reviews:
            {reviews_text}.
            Provide only the matching reviewee's ID or IDs in a comma-separated format (e.g., 1 or 1, 2) without any additional text.
            """

            prompt = system_instructions.format(
                user_preference=user_preference,
                reviews_text=reviews_text
            )

            user_preference_analysis = ask_chatgpt(user_message=prompt, system_instructions="")
            print('user_preference_analysis:', user_preference_analysis)

            # 응답 포맷 확인 및 처리
            try:
                if "Review ID:" in user_preference_analysis:
                    # "Review ID: 1, 2" 형식 처리
                    matching_reviewee_ids = [int(id.strip()) for id in user_preference_analysis.split(":")[1].split(",")]
                else:
                    # "1, 2" 형식 처리
                    matching_reviewee_ids = [int(id.strip()) for id in user_preference_analysis.split(",")]
            except (ValueError, IndexError) as e:
                raise ValueError(f"Unexpected response format from OpenAI: {user_preference_analysis}") from e

            # 유저 필터링
            if matching_reviewee_ids:  # 리스트가 비어있지 않은 경우
                users = users.filter(id__in=matching_reviewee_ids)

        # 직렬화하여 응답
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class indexView(generic.TemplateView):
    template_name = 'users/index.html'


class discordLoginView(generic.View):
    """
    디스코드 oauth2 인증 로그인
    작성자: 김우린
    작성 날짜: 2024.10.10
    """
    
    def get(self, request):
        # if the user is logged in, they will be redirected.
        if self.request.user.is_authenticated:
            return redirect("index")

        # If the 'QUERY_STRING' is > 0, that means the code is in the url ==> oauth2/login?code=********
        elif len(self.request.META['QUERY_STRING']) > 0:
            code = self.request.GET.get('code')
            getUser = self.exchangeCode(code)
            
            # 디스코드 사용자 정보로 User 검색
            user = User.objects.filter(discord_username=getUser['username'], discord_tag=getUser['discriminator']).first()

            # 사용자가 없으면 새로 생성
            if not user:
                user = User.objects.create(
                    username=getUser['username'],
                    discord_username=getUser['username'],
                    discord_tag=getUser['discriminator'],
                    email=getUser.get('email', ''),  # 이메일이 있으면 사용, 없으면 빈 문자열
                )
                user.set_unusable_password()  # 비밀번호를 사용할 수 없게 설정
                user.save()

            # 사용자의 backend 설정
            backend = get_backends()[0]  # 첫 번째 인증 백엔드 사용 (필요 시 수정)
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
            
            login(request, user)
            return redirect("user_index")

        # redirects to discord api
        else:
            return redirect(DiscordOAuth2["DISCORD_OAUTH2_URL"])

    # 디스코드 API로부터 사용자 정보를 가져오는 함수
    def exchangeCode(self, code: str):
        data = {
            "client_id": DiscordOAuth2["CLIENT_ID"],
            "client_secret": DiscordOAuth2["CLIENT_SECRET"],
            'grant_type': 'authorization_code',
            "code": code,
            "redirect_uri": DiscordOAuth2["REDIRECT_URI"],
            "scope": "identify"
        }
        
        # 토큰 요청
        response = requests.post(
            f"{DiscordOAuth2['API_ENDPOINT']}/oauth2/token", 
            data=data, 
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        # 응답 상태 및 내용 출력 (디버깅 용도)
        print(response.status_code, response.text)
        response.raise_for_status()

        # 토큰 응답을 JSON으로 파싱
        token_response = response.json()
        access_token = token_response.get('access_token')

        # 액세스 토큰이 없는 경우 예외 발생
        if access_token is None:
            raise ValueError("Access token not found in the response")
        
        # 디스코드 사용자 정보를 요청
        user_response = requests.get(
            f"{DiscordOAuth2['API_ENDPOINT']}/users/@me", 
            headers={"Authorization": f"Bearer {access_token}"}
        )
        return user_response.json()
    

