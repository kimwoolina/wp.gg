from parties.models import Parties
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import TemplateView
import requests
from django.http import Http404


# user 앱 관련

"""홈 화면 페이지 렌더링"""
def home(request):
    return render(request, 'home.html')

"""게임 선택 페이지"""
def gamechoice(request):
    return render(request, 'gamechoice.html')

"""계정 선택 페이지"""
def login_selection(request):
    return render(request, 'login_selection.html')

"""회원가입 페이지 렌더링"""
def register_page(request):
    return render(request, 'register.html')

"""로그인 페이지 렌더링"""
def login_page(request):
    return render(request, 'login.html')

"""마이페이지 조회 렌더링"""
def profile(request):
    return render(request, 'profile.html')


# profile 앱 관련
class RiotPageView(generic.TemplateView):
    template_name = 'profiles/riot.html'
    
class MatchingPageView(TemplateView):
    template_name = 'profiles/matching.html'
    
class SearchPageView(TemplateView):
    template_name = 'profiles/user_search.html'

def ranking(request):
    return render(request, 'profiles/rankings.html')

def matching_result(request):
    return render(request, 'profiles/matching.html')

class UserDetailPageView(TemplateView):
    template_name = 'profiles/user_detail.html'


# chats 앱 관련
""" 채팅방 템플릿 뷰 """
class ChatRoomTemplateView(generic.TemplateView):
    template_name = 'chats/chat.html'
    
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


def article_detail_view(request, article_id):
    # API에서 데이터 가져오기
    try:
        response = requests.get(f'http://localhost:8000/api/articles/{article_id}/')
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        article = response.json()  # JSON으로 변환
    except requests.exceptions.HTTPError:
        raise Http404("Article not found.")  # 404 오류 발생
    
    return render(request, 'articles/article_detail.html', {'article': article})


class indexView(generic.TemplateView):
    template_name = 'users/discordIndex.html'


def base(request):
    return render(request, 'base.html')
    

def party(request):
    print(request.method)
    if request.method == 'GET':
        # try:
        #     response = requests.get('http://127.0.0.1:8000/api/party/')  # 로컬 API URL
        #     response.raise_for_status()  # 오류 발생 시 예외 처리
        # except requests.exceptions.RequestException as e:
        #     return HttpResponse(f"API 요청 오류: {e}", status=500)
        
        # # API로부터 받은 JSON 데이터를 파싱
        # party_data = response.json()
        # print(party_data)
        
        # 데이터를 템플릿으로 전달하여 HTML 렌더링
        party_data = Parties.objects.all().order_by("-pk")
        return render(request, 'parties/parties.html', {'party': party_data})
    elif request.method == 'POST':
        print("post request")
        try:
            response = requests.post(f'http://localhost/api/party/', json=request.POST)
            response.raise_for_status()
        except:
            return redirect('')
        party_data = Parties.objects.all().order_by("-pk")
        return render(request, 'parties/parties.html', {'party': party_data})