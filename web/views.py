from django.shortcuts import render
from django.views import generic
from django.views.generic import TemplateView


# profile 앱 관련

class RiotPageView(generic.TemplateView):
    template_name = 'riot.html'
    
class MatchingPageView(TemplateView):
    template_name = 'users/matching.html'
    
class SearchPageView(TemplateView):
    template_name = 'users/user_search.html'

def ranking(request):
    return render(request, 'users/rankings.html')

def matching_result(request):
    return render(request, 'users/matching.html')


# chats 앱 관련

class ChatRoomTemplateView(generic.TemplateView):
    """ 채팅방 템플릿 뷰 """
    template_name = 'chats/chat.html'
    
# class ChatRoomTemplateView(APIView):
#     def get(self, request):
#         return render(request, 'chats/chat.html', {'user': request.user})
    