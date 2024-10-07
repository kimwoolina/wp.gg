from rest_framework.response import Response
from articles.serializers import ArticleSerializer
from articles.models import Articles
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from rest_framework import status


User = get_user_model()


class ArticleListAPIView(ListAPIView):
        def post(self, request): # 글 생성
                if request.user.is_authenticated:
                        req_data = request.data
                        req_files = request.FILES

                        reviewer_id = request.user.pk
                        reviewer = request.user
                        reviewee_id = int(req_data.get('reviewee'))
                        reviewee = User.objects.get(id=reviewee_id)

                        if reviewee_id == reviewer_id:
                                return Response({"message":"자기 자신에게 평가는 불가능합니다."}, status=status.HTTP_400_BAD_REQUEST)
                        if not User.objects.filter(id=reviewee_id).exists():
                                return Response({"message":"평가하려는 유저를 찾을 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
                        if Articles.objects.filter(reviewee_id=reviewee_id, reviewer_id=reviewer_id).exists():
                                return Response({"message":"한 유저에게 두번 평가는 불가능합니다."}, status=status.HTTP_400_BAD_REQUEST)

                        target_article_data = {
                                'title' : req_data.get('title'),
                                'content' : req_data.get('content'),
                                'article_score' : int(req_data.get('article_score')),
                        }

                        try:
                                serializer = ArticleSerializer(data=target_article_data, context={'request':request, 'img':req_files.getlist('img')})
                                if serializer.is_valid():
                                        article = serializer.save(reviewee=reviewee, reviewer=reviewer)
                                else:
                                        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
                        except Exception as e:
                                return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

                        # 최종적으로 생성된 아티클 데이터 반환
                        article_serializer = ArticleSerializer(article)
                        return Response(article_serializer.data, status=status.HTTP_201_CREATED)
                return Response({"message":"로그인 이후 이용 가능합니다"}, status=status.HTTP_400_BAD_REQUEST)