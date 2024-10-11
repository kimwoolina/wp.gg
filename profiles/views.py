from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework import generics
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.db.models import F, Q
from users.models import User, Evaluations
from articles.models import Articles
from .serializers import UserSerializer, EvaluationSerializer, ArticleSerializer,  UserRankingSerializer
from .bots import ask_chatgpt
from django.db import models
from django.views import generic


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


class SearchPageView(TemplateView):
    template_name = 'users/user_search.html'



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

        # 상위 3명만 선택
        users = users[:3]
        
        # 직렬화하여 응답
        serializer = UserSerializer(users, many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)
        return render(request, 'users/matching_result.html', {'users': serializer.data})

    def post(self, request, *args, **kwargs):
        # 초기화
        matching_reviewee_id = None

        # 요청에서 필터링 값 가져오기
        riot_tiers = request.data.getlist('riot_tier', [])
        positions = request.data.getlist('positions', [])
        filter_fields = request.data.getlist('filter_fields', [])
        user_preference = request.data.get('user_preference', '')

        # 기본 유저 리스트 가져오기
        users = User.objects.all()

        # 1. 기본 필터링 (티어와 포지션에 따라 필터링)
        if riot_tiers:
            users = users.filter(riot_tier__in=riot_tiers)

        if positions:
            users = users.filter(positions__position_name__in=positions)

        # 2. 평가 필드 필터링
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

        # 상위 3명만 선택
        users = users[:3]
        
        # 직렬화하여 응답
        serializer = UserSerializer(users, many=True)
        return render(request, 'users/matching_result.html', {'users': serializer.data})

class MatchingPageView(TemplateView):
    template_name = 'users/matching.html'


class indexView(generic.TemplateView):
    template_name = 'users/index.html'
