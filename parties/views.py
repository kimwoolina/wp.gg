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
    permission_classes = [IsAuthenticatedOrReadOnly]# 확인용으로 바꿈 IsAuthenticatedOrReadOnly로 바꿔줘야함

    # 팀 매칭(파티 찾기) RQ-021
    def get(self, request):
        """
        현재 존재하는 파티 보여주기
        Party안에 리스트로 보내줌 rank, age, gender, server, language등 상세 정보는 model에 적혀있음
        {
            "Party": [
                {
                    "user": 2, "rank": "0", "server": "KR", "language": "KR", "age": "10", "gender": "B", 
                    "created_at": "2024-10-07T20:38:11.910963+09:00", "is_rank": true,
                    "top1": null, "jungle1": null, "mid1": null, "support1": null, "adc1": null,
                    "top2": null, "jungle2": null, "mid2": 3, "support2": null, "adc2": null
                },
                {
                    "user": 2, "rank": "0", "server": "KR", "language": "KR", "age": "20", "gender": "M",
                    "created_at": "2024-10-07T20:36:37.840061+09:00", "is_rank": true,
                    "top1": null, "jungle1": 2, "mid1": null, "support1": null, "adc1": null,
                    "top2": null, "jungle2": null, "mid2": null, "support2": null, "adc2": null
                },
                {
                    "user": 2, "rank": "0", "server": "KR", "language": "KR", "age": "30", "gender": "F",
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
        print("\n", request.user.id, "\n")

        return Response({"Party": serializer.data})

    # 팀 생성 RQ-021-1
    def post(self, request):
        """position:mid, top, jun, adc, sup 5개중에 하나로 입력되고 그에 따라 방장의 라인이 결졍된다."""
        print(request.user, "있나?asdfas")
        if request.user.in_party is not None:
            return Response({"data":"error", "message": "이미 파티에 참여된 상태입니다."}, status=400)

        # 체크박스의 값은 on, off로 들어오는것 같다.
        is_rank = request.data.get('is_rank') == 'on'
        
        # print(f"rank:{request.data.get('rank')}, server:{request.data.get('server')}, language:{request.data.get('language')}")
        line = request.data.get("position")
        
        if line == "mid":
            party = Parties.objects.create(user=request.user, rank=request.data.get("rank"),
                                server=request.data.get("server"), language=request.data.get("language"),
                                age=request.data.get("age"), gender=request.data.get("gender"),
                                is_rank=is_rank, mid1=request.user)
        elif line == "top":
            party = Parties.objects.create(user=request.user, rank=request.data.get("rank"),
                                server=request.data.get("server"), language=request.data.get("language"),
                                age=request.data.get("age"), gender=request.data.get("gender"),
                                is_rank=is_rank, top1=request.user)
        elif line == "jun":
            party = Parties.objects.create(user=request.user, rank=request.data.get("rank"),
                                server=request.data.get("server"), language=request.data.get("language"),
                                age=request.data.get("age"), gender=request.data.get("gender"),
                                is_rank=is_rank, jungle1=request.user)
        elif line == "sup":
            party = Parties.objects.create(user=request.user, rank=request.data.get("rank"),
                                server=request.data.get("server"), language=request.data.get("language"),
                                age=request.data.get("age"), gender=request.data.get("gender"),
                                is_rank=is_rank, support1=request.user)
        elif line == "adc":
            party = Parties.objects.create(user=request.user, rank=request.data.get("rank"),
                                server=request.data.get("server"), language=request.data.get("language"),
                                age=request.data.get("age"), gender=request.data.get("gender"),
                                is_rank=is_rank, adc1=request.user)
        request.user.in_party=party.id
        print(party.id, request.user.in_party)
        request.user.save()
        serializer = PartiesSerializer(party)
        return Response({"data": serializer.data})

    def delete(self, request):
        print(request.user)
        if request.user == "AnonymousUser":
            print("사용자 정보 전달 안됨")
        pk=request.data.get("id")
        delete_party = get_object_or_404(Parties, id=pk)
        # 방장만 방 폭파 가능
        if request.user == delete_party.user:
            print("delete_party")
            if delete_party.top1:
                delete_party.top1.in_party = None
                delete_party.top1.save()
            if delete_party.jungle1:
                delete_party.jungle1.in_party = None
                delete_party.jungle1.save()
            if delete_party.mid1:
                delete_party.mid1.in_party = None
                delete_party.mid1.save()
            if delete_party.support1:
                delete_party.support1.in_party = None
                delete_party.support1.save()
            if delete_party.adc1:
                delete_party.adc1.in_party = None
                delete_party.adc1.save()
            if not delete_party.is_rank:
                print("내전")
                if delete_party.top2:
                    delete_party.top2.in_party = None
                    delete_party.top2.save()
                if delete_party.jungle2:
                    delete_party.jungle2.in_party = None
                    delete_party.jungle2.save()
                if delete_party.mid2:
                    delete_party.mid2.in_party = None
                    delete_party.mid2.save()
                if delete_party.support2:
                    delete_party.support2.in_party = None
                    delete_party.support2.save()
                if delete_party.adc2:
                    delete_party.adc2.in_party = None
                    delete_party.adc2.save()
            delete_party.save()
                
            delete_party.delete()
            return Response({"status": "succeed", "message": "delete_party", "delete_id": pk})
        else:
            print("no party master")
            return Response({"status": "dismissed", "message": "You are not the owner of this party."})


class PartyDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]# 확인용으로 바꿈 IsAuthenticatedOrReadOnly로 바꿔줘야함
    def post(self, request, party_pk):
        def putparty(id):
            if party.top1 is request.user:
                print("already in party")
            elif party.jungle1 is request.user:
                print("already in party")
            elif party.mid1 is request.user:
                print("already in party")
            elif party.support1 is request.user:
                print("already in party")
            elif party.adc1 is request.user:
                print("already in party")
            
            # 파티 중복 가능하면
            if id=="top1":
                if party.top1 is None:
                    party.top1 = request.user
                else:
                    print("error top1 not")
                    return Response({"status":"error", "message": "top already exist"})
            elif id=="jun1":
                if party.jungle1 is None:
                    party.jungle1 = request.user
                else:
                    print("error jungle1 not")
                    return Response({"status":"error", "message": "jungle already exist"})
            elif id=="mid1":
                if party.mid1 is None:
                    party.mid1 = request.user
                else:
                    print("error mid1 not")
                    return Response({"status":"error", "message": "mid already exist"})
            elif id=="sup1":
                if party.support1 is None:
                    party.support1 = request.user
                else:
                    print("error support1 not")
                    return Response({"status":"error", "message": "support already exist"})
            elif id=="adc1":
                if party.adc1 is None:
                    party.adc1 = request.user
                else:
                    print("error adc1 not")
                    return Response({"status":"error", "message": "adc already exist"})
            elif id=="top2":
                if party.top2 is None:
                    party.top2 = request.user
                else:
                    print("error top2 not")
                    return Response({"status":"error", "message": "top already exist"})
            elif id=="jun2":
                if party.jungle2 is None:
                    party.jungle2 = request.user
                else:
                    print("error jungle2 not")
                    return Response({"status":"error", "message": "jungle already exist"})
            elif id=="mid2":
                if party.mid2 is None:
                    party.mid2 = request.user
                else:
                    print("error mid2 not")
                    return Response({"status":"error", "message": "mid already exist"})
            elif id=="sup2":
                if party.support2 is None:
                    party.support2 = request.user
                else:
                    print("error support2 not")
                    return Response({"status":"error", "message": "support already exist"})
            elif id=="adc2":
                if party.adc2 is None:
                    party.adc2 = request.user
                else:
                    print("error adc2 not")
                    return Response({"status":"error", "message": "adc already exist"})
            else:
                print("error")
                return Response({"status":"error", "message": "unknown position"})
            party.save()
            print("end")
            return Response({"status":position, "i":"am"})
            # 파티 중복 불가능하면
            # if not request.user.party_top1:
            #     print("already exist")
            # elif request.user.party_top2:
            #     print("already exist")
            # elif request.user.party_mid1:
            #     print("already exist")
            # elif request.user.party_mid2:
            #     print("already exist")
            # elif request.user.party_jungle1:
            #     print("already exist")
            # elif request.user.party_jungle2:
            #     print("already exist")
            # elif request.user.party_support1:
            #     print("already exist")
            # elif request.user.party_support2:
            #     print("already exist")
            # elif request.user.party_adc1:
            #     print("already exist")
            # elif request.user.party_adc2:
            #     print("already exist")
        # print(f"{request.user.party_top1}")
        party = get_object_or_404(Parties, id=party_pk)
        position = request.data.get("position")
        print(f"id:{party.id}, user:{request.user.id}")
        if request.data.get("status") == "party in":
            return putparty(position)
        elif request.data.get("status") == "change":
            return putparty(position)

    def delete(self, request, party_pk):
        return Response({"status":party_pk})


class PartyExileView(APIView):
    # 인증(로그인)해야 이 기능 사용 가능 비로그인은 읽기 허용
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, party_pk, position, *args, **kwargs):
        party_exile = get_object_or_404(party, id=party_pk)
        party_exile.delete()

    def delete(self, request, party_pk, position):
        party_exile = get_object_or_404(party, id=party_pk)
        party_exile.delete()


# class PartyChangeView(APIView):
#     # 인증(로그인)해야 이 기능 사용 가능 비로그인은 읽기 허용
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def get(self, request):
#         pass