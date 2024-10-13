from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from articles.serializers import (
    ArticleSerializer, 
    ArticleReadSerializer, 
    CommentSerializer,
    UserSerializer
)
from articles.models import Articles, Comments
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class ArticleDetailView(RetrieveAPIView):
	queryset = Articles.objects.all()
	serializer_class = ArticleReadSerializer

class RevieweeSearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        if query:
            users = User.objects.filter(username__icontains=query) | User.objects.filter(riot_username__icontains=query)
            serializer = UserSerializer(users, many=True)
            return Response({'users': serializer.data}, status=status.HTTP_200_OK)
        return Response({'users': []}, status=status.HTTP_200_OK)

class ArticleAPIView(APIView):
	def get(self, request): # 글 리스트
		articles = Articles.objects.all()
		articles = articles.order_by('-created_at')
		serializer = ArticleSerializer(articles, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

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


class CommentAPIView(APIView):
	def get_object(self, pk):
		return get_object_or_404(Comments, pk=pk)
	
	def post(self, request, pk):		# 댓글 생성
		if request.user.is_authenticated:
			article = get_object_or_404(Articles, pk=pk)
			serializer = CommentSerializer(data=request.data)
			if serializer.is_valid(raise_exception=True):
				serializer.save(article=article, user=request.user)
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response({"message":"로그인 이후 이용 가능합니다"}, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, pk):		# 댓글 삭제
		if request.user.is_authenticated:
			comment = self.get_object(pk)
			comment.delete()
			data = {"pk": f"{pk} 삭제됨"}
			return Response(data, status=status.HTTP_200_OK)
		return Response({"message":"로그인 이후 이용 가능합니다"}, status=status.HTTP_400_BAD_REQUEST)
