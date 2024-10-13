from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from .models import Parties
from users.models import User
from .serializers import PartiesSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated, AllowAny


class PartyView(ListCreateAPIView):
    serializer_class = PartiesSerializer
    # 인증(로그인)해야 이 기능 사용 가능 비로그인은 읽기 허용
    permission_classes = [AllowAny]# 확인용으로 바꿈 IsAuthenticatedOrReadOnly로 바꿔줘야함

    # 팀 매칭(파티 찾기) RQ-021
    def get(self, request):
        """
        현재 존재하는 파티 보여주기
        Party안에 리스트로 보내줌 rank, age, gender, server, language등 상세 정보는 model에 적혀있음
        {
            "Party": [
                {
                    "rank": "0", "server": "KR", "language": "KR", "age": "00", "gender": "B", 
                    "created_at": "2024-10-07T20:38:11.910963+09:00", "is_rank": true,
                    "top1": null, "jungle1": null, "mid1": null, "support1": null, "adc1": null,
                    "top2": null, "jungle2": null, "mid2": 3, "support2": null, "adc2": null
                },
                {
                    "rank": "0", "server": "KR", "language": "KR", "age": "00", "gender": "B",
                    "created_at": "2024-10-07T20:36:37.840061+09:00", "is_rank": true,
                    "top1": null, "jungle1": 2, "mid1": null, "support1": null, "adc1": null,
                    "top2": null, "jungle2": null, "mid2": null, "support2": null, "adc2": null
                },
                {
                    "rank": "0", "server": "KR", "language": "KR", "age": "00", "gender": "B",
                    "created_at": "2024-10-07T20:23:28.912341+09:00", "is_rank": false,
                    "top1": 1, "jungle1": null, "mid1": null, "support1": null, "adc1": null,
                    "top2": null, "jungle2": null, "mid2": null, "support2": null, "adc2": null
                } 
            ] 
        }
        """
        parties = Parties.objects.all().order_by("-pk")
        # print(f"\n\n{parties}\n\n")
        serializer = PartiesSerializer(parties, many=True)
        # keys = serializer.data["Party"]
        tior = {
            "0": "Unranked",
            "1": "Iron",
            "2": "Bronze",
            "3": "Silver",
            "4": "Gold",
            "5": "Platinum",
            "6": "Amarald",
            "7": "Diamond",
            "8": "Master",
            "9": "Grand Master",
            "10": "Challenger"
        }
        print("\n", request.user.id, "\n")
        # for i in serializer.data:
        #     print(f"rank:{i['rank']}, server:{i['server']}, language:{i['language']}, age:{i['age']}, gender:{i['gender']}, is_rank:{i['is_rank']}, top1:{i['top1']}, jungle1:{i['jungle1']}, mid1:{i['mid1']}, support1:{i['support1']}, adc1:{i['adc1']}, top2:{i['top2']}, jungle2:{i['jungle2']}, mid2:{i['mid2']}, support2:{i['support2']}, adc2:{i['adc2']}, user:{i['user']}")
        # pure django
        return render(request, "parties/parties.html", {"party":parties, "tior":tior})
        # rest api
        # return Response({"Party": serializer.data})

    # 팀 생성 RQ-021-1
    def post(self, request):
        """position:mid, top, jun, adc, sup 5개중에 하나로 입력되고 그에 따라 방장의 라인이 결졍된다."""

        # 체크박스의 값은 on, off로 들어오는것 같다.
        is_rank = request.data.get('is_rank') == 'on'

        # print(f"rank:{request.data.get('rank')}, server:{request.data.get('server')}, language:{request.data.get('language')}")
        line = request.data.get("position")
        
        # 로그인 안되면 확인용
        if line == "mid":
            party = Parties.objects.create(user=User.objects.get(id=2), rank=request.data.get("rank"),
                                server=request.data.get("server"), language=request.data.get("language"),
                                age=request.data.get("age"), gender=request.data.get("gender"),
                                is_rank=is_rank, mid1=User.objects.get(id=2))
        elif line == "top":
            party = Parties.objects.create(user=User.objects.get(id=2), rank=request.data.get("rank"),
                                server=request.data.get("server"), language=request.data.get("language"),
                                age=request.data.get("age"), gender=request.data.get("gender"),
                                is_rank=is_rank, top1=User.objects.get(id=2))
        elif line == "jun":
            party = Parties.objects.create(user=User.objects.get(id=2), rank=request.data.get("rank"),
                                server=request.data.get("server"), language=request.data.get("language"),
                                age=request.data.get("age"), gender=request.data.get("gender"),
                                is_rank=is_rank, jungle1=User.objects.get(id=2))
        elif line == "sup":
            party = Parties.objects.create(user=User.objects.get(id=2), rank=request.data.get("rank"),
                                server=request.data.get("server"), language=request.data.get("language"),
                                age=request.data.get("age"), gender=request.data.get("gender"),
                                is_rank=is_rank, support1=User.objects.get(id=2))
        elif line == "adc":
            party = Parties.objects.create(user=User.objects.get(id=2), rank=request.data.get("rank"),
                                server=request.data.get("server"), language=request.data.get("language"),
                                age=request.data.get("age"), gender=request.data.get("gender"),
                                is_rank=is_rank, adc1=User.objects.get(id=2))
        
        
        # 로그인 되면 이거로 바꾸기
        # if line == "mid":
        #     party = Parties.objects.create(user=request.user, rank=request.data.get("rank"),
        #                         server=request.data.get("server"), language=request.data.get("language"),
        #                         age=request.data.get("age"), gender=request.data.get("gender"),
        #                         is_rank=is_rank, mid1=request.user)
        # elif line == "top":
        #     party = Parties.objects.create(user=request.user, rank=request.data.get("rank"),
        #                         server=request.data.get("server"), language=request.data.get("language"),
        #                         age=request.data.get("age"), gender=request.data.get("gender"),
        #                         is_rank=is_rank, top1=request.user)
        # elif line == "jun":
        #     party = Parties.objects.create(user=request.user, rank=request.data.get("rank"),
        #                         server=request.data.get("server"), language=request.data.get("language"),
        #                         age=request.data.get("age"), gender=request.data.get("gender"),
        #                         is_rank=is_rank, jungle1=request.user)
        # elif line == "sup":
        #     party = Parties.objects.create(user=request.user, rank=request.data.get("rank"),
        #                         server=request.data.get("server"), language=request.data.get("language"),
        #                         age=request.data.get("age"), gender=request.data.get("gender"),
        #                         is_rank=is_rank, support1=request.user)
        # elif line == "adc":
        #     party = Parties.objects.create(user=request.user, rank=request.data.get("rank"),
        #                         server=request.data.get("server"), language=request.data.get("language"),
        #                         age=request.data.get("age"), gender=request.data.get("gender"),
        #                         is_rank=is_rank, adc1=request.user)
        
        # pure django
        return redirect("parties:create_party")
    
        # rest api
        # serializer = PartiesSerializer(party)
        # return Response({"data": serializer.data})


class PartyDetailView(APIView):
    permission_classes = [AllowAny]# 확인용으로 바꿈 IsAuthenticatedOrReadOnly로 바꿔줘야함

    def delete(self, request, party_pk):
        print(request.user)
        delete_party = get_object_or_404(Parties, id=party_pk)
        # 확인용
        print("요청접수")
        # 방장만 방 폭파 가능
        if request.user == delete_party.user:
            print("delete_party")
            delete_party.delete()
            return Response({"status": "succeed", "message": "delete_party", "delete_id": party_pk})
        else:
            print("no party master")
            return Response({"status": "dismissed", "message": "You are not the owner of this party."})


class PartyExileView(APIView):
    # 인증(로그인)해야 이 기능 사용 가능 비로그인은 읽기 허용
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, request, party_pk, position):
        party_exile = get_object_or_404(party, id=party_pk)
        party_exile.delete()


# class PartyChangeRankView(APIView):
#     # 인증(로그인)해야 이 기능 사용 가능 비로그인은 읽기 허용
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def get(self, request):
#         pass