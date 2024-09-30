from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.registration.views import RegisterView
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, EvaluationSerializer, ArticleSerializer
from rest_framework import generics
from .models import Evaluations
from articles.models import Articles 


# 회원가입
class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        # 회원가입 완료시 메시지
        if response.status_code == status.HTTP_204_NO_CONTENT:
            response = Response({"message": "회원가입이 완료되었습니다😊"}, status=status.HTTP_201_CREATED)
        
        # if response.status_code == status.HTTP_201_CREATED:
        #     response.data['message'] = '회원가입이 완료되었습니다😊'
        
        return response

# 로그인
class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_200_OK:
            user = self.request.user
            username = user.username

            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response.data = {
                'message': f'{username}님 안녕하세요😊',
                'access': access_token,
                'refresh': refresh_token
            }
            
            # access_token, refresh_token 없으면 에러 메시지 
            if not access_token or not refresh_token:
                response.data['error'] = '토큰을 발급받지 못했습니다.'

        return response
    
# 로그아웃
class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):

        return Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)


# 회원탈퇴
User = get_user_model()

class CustomDeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]  

    def delete(self, request, *args, **kwargs):
        user = request.user  
        user.delete() # 유저 정보 아예 삭제할건지 팀원들과 이야기해봐야 함

        logout(request)

        return Response({"message": "회원탈퇴 완료! 그동안 이용해주셔서 감사했습니다👋"}, status=status.HTTP_200_OK)
    


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
        