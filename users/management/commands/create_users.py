import random
from faker import Faker
from tqdm import tqdm

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from users.models import Positions, Platform, Evaluations

fake = Faker(locale="ko_KR")
User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        user_list = []
        riot_tiers = [
            'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'EMERALD',
            'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER'
        ]
        positions = ['top', 'jungle', 'mid', 'adc', 'support', 'bottom']
        positions_cache = {pos_name: Positions.objects.get_or_create(position_name=pos_name)[0] for pos_name in positions}

        for __ in tqdm(range(100), desc="유저 생성"):
            email = fake.email()
            username_base = email.split('@')[0]
            username = username_base

            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{username_base}_{counter}"
                counter += 1

            password = username

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                riot_tag=random.choice(['KR1']),
                introduction=fake.sentence(),
                score=round(random.uniform(0, 10), 2),
                riot_tier=random.choice(riot_tiers),
            )

            selected_positions = random.sample(positions, random.randint(1, len(positions)))

            for position in selected_positions:
                user.positions.add(positions_cache[position])

            user_list.append(user)

            Evaluations.objects.create(
                user=user,
                kindness=random.randint(0, 10),
                teamwork=random.randint(0, 10),
                communication=random.randint(0, 10),
                mental_strength=random.randint(0, 10),
                punctuality=random.randint(0, 10),
                positivity=random.randint(0, 10),
                mvp=random.randint(0, 10),
                mechanical_skill=random.randint(0, 10),
                operation=random.randint(0, 10),
                negativity=random.randint(0, 10),
                profanity=random.randint(0, 10),
                afk=random.randint(0, 10),
                cheating=random.randint(0, 10),
                verbal_abuse=random.randint(0, 10),
            )