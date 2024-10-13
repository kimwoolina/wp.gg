from django.core.exceptions import ValidationError
import re

def validate_email(value):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, value):
        raise ValidationError("유효하지 않은 이메일 형식입니다.")

def validate_username_length(value):
    if len(value) < 3 or len(value) > 15:
        raise ValidationError("유저네임은 3자 이상, 15자 이하로 입력해주세요.")
