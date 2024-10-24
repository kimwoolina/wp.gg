from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.db.models import F, Q
from users.models import User, Evaluations, Positions
from articles.models import Articles
from .serializers import ( UserSerializer, EvaluationSerializer, 
                        ArticleSerializer,  UserRankingSerializer )
from .bots import ask_chatgpt
from .riot import get_user_info
from django.db import models
from rest_framework.permissions import AllowAny
from wpgg.settings import RIOT_API_KEY
import re
import logging

logger = logging.getLogger('django') 


class UserDetailView(generics.GenericAPIView):
    """
    유저를 검색하여 해당하는 유저의 상세정보 + 라이엇 정보 조회
    작성자: 김우린
    작성 날짜: 2024.09.30

    메서드:
    GET: 특정 사용자의 riot_username과 riot_tag에 따른 정보를 반환하고,
    라이엇 정보와 비교하여 user.riot_iag, user.positions에 값 저장
    """
    
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        riot_tag = request.query_params.get('riot_tag')

        # 사용자 검색을 위한 필터
        filters = {}

        if riot_tag:  # riot_tag가 있는 경우
            filters['riot_username'] = username
            filters['riot_tag'] = riot_tag
        else:  # riot_tag가 없는 경우
            filters['riot_username'] = username
            
            # 쿼리셋 생성
            user_queryset = User.objects.filter(**filters)

            # 유저를 찾지 못한 경우, username을 기준으로 다시 필터링
            if not user_queryset.exists():
                filters = {'username': username}  # username으로만 필터링
                user_queryset = User.objects.filter(**filters)
        
        # 사용자 검색
        user_queryset = User.objects.filter(**filters)

        if user_queryset.exists():
            user = user_queryset.first()
            # 라이엇 정보 가져오기
            user_info = self.get_riot_info(user, username, riot_tag)
            
            if not user_info:
                logger.error(f'Riot API로부터 사용자 정보 조회 실패: {username}, {riot_tag}')
                
            # reviewee로서 해당 사용자가 작성한 게시글 목록 가져오기
            articles = Articles.objects.filter(reviewee=user)
            serializer_data = self.get_serializer_data(user, articles)

            # 라이엇 정보 추가
            if riot_tag and user_info:
                serializer_data['riot_info'] = user_info
            
            return Response(serializer_data)

        logger.error(f"소환사 '{username}'에 대한 정보를 찾을 수 없습니다.")
        return Response({"message": f"{username} 소환사에 대한 정보를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    def get_riot_info(self, user, username, riot_tag):
        if riot_tag:  # riot_tag가 있는 경우에만 라이엇 정보 호출
            user_info = get_user_info(RIOT_API_KEY, username, riot_tag)
            if 'error' in user_info:
                return None
            
            # 라이엇 프로필 이미지 저장
            self.update_user_with_riot_info(user, user_info)
            return user_info
        return None

    def update_user_with_riot_info(self, user, user_info):
        profile_icon_link = user_info.get('profileIconLink')
        if profile_icon_link:
            user.riot_profile_image = profile_icon_link
            user.save()

        league_info = user_info.get('league', [])
        if league_info:
            tier = league_info[0].get('tier')
            if tier and tier != user.riot_tier:
                user.riot_tier = tier
                user.save()

        preferred_position = user_info.get('preferredPosition')
        if preferred_position:
            user.position = preferred_position.lower()  # position 필드에 값 저장
            user.save()

    def get_serializer_data(self, user, articles):
        serializer = self.get_serializer(user)
        serializer_data = serializer.data

        # Evaluations를 serializer_data에 추가
        evaluations = self.get_evaluations(user)
        serializer_data['evaluations'] = evaluations

        # articles를 serializer_data에 추가
        article_serializer = ArticleSerializer(articles, many=True)
        serializer_data['articles'] = article_serializer.data

        return serializer_data

    def get_evaluations(self, user):
        try:
            evaluations = Evaluations.objects.get(user=user)
            evaluations_data = EvaluationSerializer(evaluations).data
        except Evaluations.DoesNotExist:
            evaluations_data = self.default_evaluations()

        # 각 필드에 대해 None이면 기본값 0으로 설정
        return {field: evaluations_data.get(field, 0) for field in [
            'kindness', 'teamwork', 'communication', 'mental_strength', 
            'punctuality', 'positivity', 'mvp', 'mechanical_skill', 
            'operation', 'negativity', 'profanity', 'afk', 
            'cheating', 'verbal_abuse'
        ]}

    def default_evaluations(self):
        return {
            'kindness': 0,
            'teamwork': 0,
            'communication': 0,
            'mental_strength': 0,
            'punctuality': 0,
            'positivity': 0,
            'mvp': 0,
            'mechanical_skill': 0,
            'operation': 0,
            'negativity': 0,
            'profanity': 0,
            'afk': 0,
            'cheating': 0,
            'verbal_abuse': 0,
        }


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
            'punctuality': 'evaluations__punctuality',  # 오타 수정
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

        # 포지션 필터링 처리 (단일 값으로 전달됨)
        position = request.query_params.get('positions')  # 단일 값으로 처리

        # 리뷰가 존재하는 유저 정보만 가져오기
        queryset = User.objects.filter(evaluations__isnull=False).select_related('evaluations')

        # 포지션 필터링 (단일 값으로 필터링)
        if position:
            queryset = queryset.filter(positions__position_name=position) # position 필드로 필터링
        # 쿼리셋을 정렬
        queryset = queryset.order_by(F(sort_by_field).desc(nulls_last=True))

        # 쿼리셋이 비어 있을 경우 메시지와 빈 리스트를 반환
        if not queryset.exists():
            return Response({"message": "해당 조건에 맞는 유저 정보가 없습니다.", "users": []}, status=status.HTTP_200_OK)

        # 정상적인 결과가 있을 경우
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



    
class UserRecommendationView(APIView):
    """
    티어, 포지션, 평가항목 선택하고 원하는 유저 상을 입력하여 유저 매칭해줌
    작성자: 김우린
    작성 날짜: 2024.10.09
    """

    def post(self, request, *args, **kwargs):
        # 초기화
        matching_reviewee_id = None

        # 요청에서 필터링 값 가져오기
        riot_tiers = request.data.get('riot_tier')
        positions = request.data.get('riot_position', [])
        filter_fields = [field for field in request.data.get('selected_categories', '').split(',') if field]
        user_preference = request.data.get('user_preference', '')
        
        # 기본 유저 리스트 가져오기
        users = User.objects.all()
        
        # 1. 기본 필터링 (티어와 포지션에 따라 필터링)
        if riot_tiers:
            users = users.filter(riot_tier=riot_tiers)

        if positions:
            users = users.filter(positions__position_name=positions)

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

        # 리뷰 데이터 가져오기
        all_reviews = Articles.objects.all().values('content', 'reviewee')
        reviews_text = "\n".join([f"Review ID: {review['reviewee']} - {review['content']}" for review in all_reviews])

        # 3. 사용자 입력 텍스트 처리
        if user_preference:
            # OpenAI API를 사용하여 유저의 선호도에 맞는 리뷰 분석
            system_instructions = """ 당신은 사용자의 선호에 따라 관련성 높은 리뷰를 찾는 임무를 맡고 있습니다. 사용자의 선호를 기반으로 다음 설명과 잘 일치하는 리뷰를 모두 찾으세요: {user_preference}. 여기 모든 리뷰가 있습니다: {reviews_text}.일치하는 리뷰어의 ID 또는 IDs를 쉼표로 구분하여 제공합니다 (예: 1 또는 1, 2) 추가 텍스트 없이.
                                """
            # system_instructions = """
            # You are tasked with finding the most relevant review for a user based on their preferences.
            # Based on the user's preference, identify the review that best matches the following description: {user_preference}.
            # Here are all the reviews:
            # {reviews_text}.
            # Provide only the matching reviewee's ID or IDs in a comma-separated format (e.g., 1 or 1, 2) without any additional text.
            # """

            prompt = system_instructions.format(
                user_preference=user_preference,
                reviews_text=reviews_text
            )

            user_preference_analysis = ask_chatgpt(user_message=prompt, system_instructions="")
            print("user_preference_analysis", user_preference_analysis)

            # 정규 표현식을 사용하여 숫자 추출
            matching_reviewee_ids = [int(num) for num in re.findall(r'\d+', user_preference_analysis)]
            matching_reviewee_ids = list(set(matching_reviewee_ids))
            # 유저 필터링
            if matching_reviewee_ids:  # 리스트가 비어있지 않은 경우
                users = users.filter(id__in=matching_reviewee_ids)
            else:
                return Response({"message": "매칭되는 유저가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)   
            
        # 상위 3명만 선택
        users = users[:3]
        
        # 직렬화하여 응답
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return render(request, 'profiles/matching_result.html', {'users': serializer.data})


class GetRiotInfoView(APIView):
    def get(self, request):
        riot_username = request.query_params.get('riot_id')
        tag_line = request.query_params.get('tag_line')

        if not riot_username or not tag_line:
            return Response({"message": "유효하지 않은 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)

        user_info = get_user_info(RIOT_API_KEY, riot_username, tag_line)

        if 'error' in user_info:
            return Response({"message": "소환사에 대한 정보를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        return Response(user_info, status=status.HTTP_200_OK)
