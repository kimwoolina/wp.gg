from rest_framework.views import APIView
from rest_framework.response import Response
from articles.serializers import ArticleSerializer, ArticleImageSerializer
from articles.models import ArticleImages
from rest_framework.generics import ListAPIView
from users.models import Evaluations
from django.contrib.auth import get_user_model
from users.serializers import EvaluationSerializer
from rest_framework import status


User = get_user_model()


class ArticleListAPIView(ListAPIView):
        def post(self, request): # 글 생성
                if request.user.is_authenticated:
                        req_data = request.data
                        req_files = request.FILES

                        reviewee_id = int(req_data.get('reviewee'))
                        reviewee = User.objects.get(id=reviewee_id)

                        if reviewee_id == request.user.pk:
                                return Response({"message":"자기 자신에게 평가는 불가능합니다."}, status=status.HTTP_400_BAD_REQUEST)
                        if not User.objects.filter(id=reviewee_id).exists():
                                return Response({"message":"평가하려는 유저를 찾을 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

                        target_article_data = {
                                'title' : req_data.get('title'),
                                'content' : req_data.get('content'),
                                'article_score' : int(req_data.get('article_score')),
                                'reviewee' : int(req_data.get('reviewee')),
                        }

                        try:
                                serializer = ArticleSerializer(data=target_article_data, context={'request':request, 'img':req_files.getlist('img')})
                                if serializer.is_valid():
                                        article = serializer.save(reviewer=request.user)
                                else:
                                        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
                        except Exception as e:
                                return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

                        target_evaluation_data = {
                                'kindness': int(req_data.get('kindness', 0)),
                                'teamwork': int(req_data.get('teamwork', 0)),
                                'communication': int(req_data.get('communication', 0)),
                                'mental_strength': int(req_data.get('mental_strength', 0)),
                                'punctualiity': int(req_data.get('punctualiity', 0)),
                                'positivity': int(req_data.get('positivity', 0)),
                                'mvp': int(req_data.get('mvp', 0)),
                                'mechanical_skill': int(req_data.get('mechanical_skill', 0)),
                                'operation': int(req_data.get('operation', 0)),
                                'negativity': int(req_data.get('negativity', 0)),
                                'profanity': int(req_data.get('profanity', 0)),
                                'afk': int(req_data.get('afk', 0)),
                                'cheating': int(req_data.get('cheating', 0)),
                                'verbal_abuse': int(req_data.get('verbal_abuse', 0)),
                                }

                        try:
                                if Evaluations.objects.filter(user_id=reviewee_id).exists():
                                        target_evaluation = Evaluations.objects.get(user_id=reviewee_id)
                                        serializer = EvaluationSerializer(target_evaluation, data=target_evaluation_data, partial=True)
                                        if serializer.is_valid():
                                                serializer.save()
                                        else:
                                                return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
                                else:
                                        serializer = EvaluationSerializer(data=target_evaluation_data)
                                        if serializer.is_valid():
                                                serializer.save(user=reviewee)
                                        else:
                                                return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
                        except Exception as e:
                                return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

                        # 최종적으로 생성된 아티클 데이터 반환
                        article_serializer = ArticleSerializer(article)
                        return Response(article_serializer.data, status=status.HTTP_201_CREATED)
                return Response({"message":"로그인 이후 이용 가능합니다"}, status=status.HTTP_400_BAD_REQUEST)