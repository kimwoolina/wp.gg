import random
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from users.models import Positions


#모든 유저들의 포지션 top으로 할당

class Command(BaseCommand):

    def handle(self, *args, **options):
        # 여러 유저를 랜덤으로 가져오기
        users = get_user_model().objects.all()  # 모든 유저 가져오기

        # 특정 포지션을 랜덤으로 선택 (예: position_name="top"인 포지션 중 하나)
        positions_queryset = Positions.objects.filter(position_name="top")

        # 각 유저에게 랜덤 포지션을 할당
        for user in users:
            if positions_queryset.exists():
                random_position = random.choice(positions_queryset)  # 포지션 중 하나를 랜덤으로 선택
                user.positions.add(random_position)  # 선택된 포지션을 유저에 추가
                user.save()

        print("랜덤 포지션이 모든 유저에게 할당되었습니다.")
