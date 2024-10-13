from django.shortcuts import render
from django.views import generic
from django.views.generic import TemplateView

# user 앱 관련



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
class ChatRoomTemplateView(generic.TemplateView):
    """ 채팅방 템플릿 뷰 """
    template_name = 'chat.html'
    
# class ChatRoomTemplateView(APIView):
#     def get(self, request):
#         return render(request, 'chats/chat.html', {'user': request.user})

# articles 앱 관련
def article_detail_page(request):
	return render(request, 'articles/article_detail.html')

def article_list_page(request):
	return render(request, 'articles/article_list.html')

def article_create_page(request):
	return render(request, "articles/article_create.html")
    