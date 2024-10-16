from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from articles.serializers import (
    ArticleSerializer,
    ArticleListSerializer,
    ArticleDetailSerializer,
    CommentSerializer,
    UserSerializer
)
from articles.models import Articles, Comments
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

class ArticleDetailView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, pk):  # URL에서 article_id를 받아옵니다.
        article = get_object_or_404(Articles, id=pk)  # ID로 기사 찾기
        serializer = ArticleDetailSerializer(article)  # Serializer를 사용하여 데이터 변환
        return Response(serializer.data, status=status.HTTP_200_OK)  # JSON 응답 반환


class RevieweeSearchView(APIView):
    """
    username 또는 riot_username으로 평가할 유저 검색 (본인 제외)
    작성자: 김우린
    작성 날짜: 2024.10.14
    """

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        current_user = request.user  # 현재 로그인한 사용자

        if query:
            # username 또는 riot_username으로 검색하고, 본인은 제외
            users = (User.objects.filter(username__icontains=query) | User.objects.filter(riot_username__icontains=query)).exclude(id=current_user.id)
            serializer = UserSerializer(users, many=True)
            return Response({'users': serializer.data}, status=status.HTTP_200_OK)
        return Response({'users': []}, status=status.HTTP_200_OK)


class ArticleAPIView(APIView):
    """
    - get: 리뷰글 목록
    - post: 리뷰 글 생성
    작성자: 김우린
    작성 날짜: 2024.10.14
    """
    
    def get(self, request):  # 글 리스트
        articles = Articles.objects.all()
        articles = articles.order_by('-created_at')
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"message": "로그인 이후 이용 가능합니다"}, status=status.HTTP_400_BAD_REQUEST)

        req_data = request.data
        req_files = request.FILES

        reviewer = request.user
        reviewee_id = req_data.get('reviewee')
        
        # 유효성 검사
        if self._is_invalid_review(reviewer.pk, reviewee_id):
            return Response({"message": "평가가 불가능한 유저입니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            article = self._create_article(req_data, req_files, reviewer, reviewee_id, request)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # 최종적으로 생성된 아티클 데이터 반환
        article_serializer = ArticleSerializer(article)
        return Response(article_serializer.data, status=status.HTTP_201_CREATED)

    def _is_invalid_review(self, reviewer_id, reviewee_id):
        if reviewer_id == reviewee_id:
            return True
        if not User.objects.filter(id=reviewee_id).exists():
            return True
        if Articles.objects.filter(reviewee_id=reviewee_id, reviewer_id=reviewer_id).exists():
            return True
        return False

    def _create_article(self, req_data, req_files, reviewer, reviewee_id, request):
        reviewee = get_object_or_404(User, id=reviewee_id)  # 유저가 존재하지 않으면 404 에러 발생
        serializer = ArticleSerializer(data=req_data, context={'request': request, 'img': req_files.getlist('img')})

        if not serializer.is_valid():
            raise ValueError(serializer.errors)  # 유효하지 않은 경우 예외 발생

        return serializer.save(reviewee=reviewee, reviewer=reviewer)


class CommentAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Comments, pk=pk)
    
    def post(self, request, pk):  # 댓글 생성
        if request.user.is_authenticated:
            article = get_object_or_404(Articles, pk=pk)
                
            serializer = CommentSerializer(data=request.data)
            
            if serializer.is_valid(raise_exception=True):
                serializer.save(article=article, user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"message": "로그인 이후 이용 가능합니다"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):  # 댓글 삭제
        if request.user.is_authenticated:
            comment = self.get_object(pk)
            comment.delete()
            data = {"pk": f"{pk} 삭제됨"}
            return Response(data, status=status.HTTP_200_OK)
        return Response({"message": "로그인 이후 이용 가능합니다"}, status=status.HTTP_400_BAD_REQUEST)
