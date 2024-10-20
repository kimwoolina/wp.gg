from parties.models import Parties
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import TemplateView
from articles.models import Articles, ArticleImages, Comments
from articles.serializers import ArticleDetailSerializer, ArticleImageSerializer, CommentSerializer
import requests
from django.http import Http404
from django.http import HttpResponseNotFound


def custom_page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

# user 앱 관련

"""홈 화면 페이지 렌더링"""
def home(request):
    return render(request, 'home.html')

"""게임 선택 페이지"""
def gamechoice(request):
    return render(request, 'users/gamechoice.html')

"""계정 선택 페이지"""
def login_selection(request):
    return render(request, 'users/login_selection.html')

"""회원가입 페이지 렌더링"""
def register_page(request):
    return render(request, 'users/register.html')

"""로그인 페이지 렌더링"""
def login_page(request):
    return render(request, 'users/login.html')

"""마이페이지 조회 렌더링"""
def profile(request):
    return render(request, 'users/profile.html')


# profile 앱 관련
class RiotPageView(generic.TemplateView):
    template_name = 'profiles/riot.html'
    
class MatchingPageView(TemplateView):
    template_name = 'profiles/matching.html'
    
class SearchPageView(TemplateView):
    template_name = 'profiles/user_search.html'

def ranking(request):
    return render(request, 'profiles/rankings.html')

def matching(request):
    return render(request, 'profiles/matching.html')

def matching_result(request):
    return render(request, 'profiles/matching_result.html')

class UserRecommendationView(TemplateView):
    template_name = 'profiles/matching_result.html'

class UserDetailPageView(TemplateView):
    template_name = 'profiles/user_detail.html'


# chats 앱 관련
""" 채팅방 템플릿 뷰 """
def chat_room_template(request):
    return render(request, 'chats/chat.html')

# class ChatRoomTemplateView(APIView):
#     def get(self, request):
#         return render(request, 'chats/chat.html', {'user': request.user})

# articles 앱 관련
def article_detail_page(request):
	return render(request, 'articles/article_detail.html')

def article_list_page(request):
	return render(request, 'articles/article_list.html')

def article_create_page(request):
	return render(request, 'articles/article_create.html')


# def article_detail_view(request, article_id):
#     # # API에서 데이터 가져오기
#     # try:
#     #     response = requests.get(f'http://localhost:8000/api/articles/{article_id}/')
#     #     # response = requests.get(f'http://43.201.57.125/api/articles/{article_id}/')
#     #     response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
#     #     article = response.json()  # JSON으로 변환
#     # except requests.exceptions.HTTPError:
#     #     raise Http404("Article not found.")  # 404 오류 발생
    
#     return render(request, 'articles/article_detail.html', {'article': article})


def article_detail_view(request, article_id):
    # API에서 데이터 가져오기
    article = get_object_or_404(Articles, id=article_id)
    
    # 관련된 이미지들 가져오기
    article_images = ArticleImageSerializer(article.article_images.all(), many=True).data
    comments = CommentSerializer(article.comments.all(), many=True).data
    
    # ArticleDetailSerializer를 사용하여 article 정보를 직렬화
    article_serializer = ArticleDetailSerializer(article)
    
    # 시리얼라이저를 사용해서 반환된 데이터들을 템플릿에 전달
    return render(request, 'articles/article_detail.html', {
        'article': article_serializer.data,  # ArticleDetailSerializer로 직렬화된 데이터
        'article_images': article_images,  # ArticleImageSerializer로 직렬화된 이미지 데이터
        'comments': comments,  # CommentSerializer로 직렬화된 댓글 데이터
    })

def base(request):
    return render(request, 'base.html')
    

def party(request):
    print(request.method)
    party_data = Parties.objects.all().order_by("-pk")
    return render(request, 'parties/parties.html', {'party': party_data})
