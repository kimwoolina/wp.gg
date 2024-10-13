from django.shortcuts import render
from django.views import generic
from django.views.generic import TemplateView

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
    template_name = 'riot.html'
    
class MatchingPageView(TemplateView):
    template_name = 'matching.html'
    
class SearchPageView(TemplateView):
    template_name = 'user_search.html'

def ranking(request):
    return render(request, 'rankings.html')

def matching_result(request):
    return render(request, 'matching.html')


# chats 앱 관련
""" 채팅방 템플릿 뷰 """
class ChatRoomTemplateView(generic.TemplateView):
    template_name = 'chat.html'
    
# class ChatRoomTemplateView(APIView):
#     def get(self, request):
#         return render(request, 'chats/chat.html', {'user': request.user})

# articles 앱 관련
def article_detail_page(request):
	return render(request, 'article_detail.html')

def article_list_page(request):
	return render(request, 'article_list.html')

def article_create_page(request):
	return render(request, 'article_create.html')


class indexView(generic.TemplateView):
    template_name = 'users/index.html'
