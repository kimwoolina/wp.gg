from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Chats(models.Model):
    sender = models.ForeignKey(User, related_name='sent_chats', on_delete=models.CASCADE)  
    receiver = models.ForeignKey(User, related_name='received_chats', on_delete=models.CASCADE)  
    content = models.TextField()  
    is_read = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 

    def mark_as_read(self):
        """메시지 읽음 표시"""
        self.is_read = True  
        self.save()

    def filter_profanity(self):
        """금지어 필터링 및 치환"""
        profanity_list = [
            "바보", "병신", "ㅂㅅ", "ㅅㅂ", "씨발", "개새끼", "ㄱㅅㄲ", "쓰레기", "좆", "좆같다", "미친", "애미", "미친놈", 
            "나쁜놈", "시발", "싸가지", "대가리", "씹", "지랄", "엿먹어라", "바퀴벌레", "찌질이", "ㅆ", "역겹", "ㅅㄲ", "ㄱㅅ",
            "정신병", "겁쟁이", "창녀", "썅", "빡대가리", "개같은", "병자", "염병", "이따위", "인생망", "찌질", "한심", "새끼" 
            "쌍놈", "그지", "똥", "거지", "하수구", "노무", "개소리", "존나", "ㅈㄴ", "넌뭐임", "ㅈㄴ", "ㄲㅈ", "바퀴벌레"]

        for word in profanity_list:
            self.content = self.content.replace(word, '🫣🫣')  # 금지어 이모티콘으로 치환
            self.save()

    def __str__(self):
        return f'{self.receiver}님! {self.sender}님이 메시지를 보냈어요💌'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='u_noti') 
    chat = models.ForeignKey(Chats, null=True, blank=True, related_name='c_noti', on_delete=models.CASCADE) 
    is_read = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(null=True, blank=True)  # 경고 메시지 저장할 필드  

    def mark_as_read(self):
        """알림 읽음 표시 후 해당 채팅도 읽음 상태로 업데이트"""
        self.is_read = True
        self.save()

        if self.chat:
            self.chat.mark_as_read() 

    def __str__(self):
        if self.chat:
            return f'{self.chat.receiver}님, {self.chat.sender}님에게 새 메시지가 왔습니다!'
        return f'{self.user}님 새로운 알림을 확인해보세요📮'


class Reports(models.Model):
    chat = models.ForeignKey(Chats, on_delete=models.CASCADE)  # 신고된 채팅 (FK)
    reporter = models.ForeignKey(User, related_name='reports_made', on_delete=models.CASCADE)  # 신고하는 사람 (FK)
    reported = models.ForeignKey(User, related_name='reports_received', on_delete=models.CASCADE)  # 신고당한 사람 (FK)
    content = models.TextField()  # 신고 내용
    created_at = models.DateTimeField(auto_now_add=True)

    def increment_warning(self):
        """신고된 사용자 및 10회 이상 나쁜 말 쓴 유저에게 경고"""
        report_count = Reports.objects.filter(reported=self.reported).count()  # 신고 횟수 확인
        if report_count >= 3:
            # 경고 메시지 전송
            self.send_warning_message()  
            # LLM 적용 예정!
            self.apply_llm_moderation()
        self.save()

    def send_warning_message(self):
        """신고된 유저에게 보내는 경고 메시지"""
        warning_message = f'{self.reported}님 10번이나 나쁜말을 사용하셨네요🥲 화나는 일이 있으셨나요? 
        {self.reported}님이 예쁜 말 고운 말을 쓸 수 있게 하루동안 wp.gg가 도와드릴게요! 채팅 속도가 미세하게 느려질 수도 있어요!'
        
        # 경고 메시지 전송 로직 (알림 테이블에 저장)
        Notification.objects.create(
            user=self.reported,  # 신고당한 유저
            chat=self.chat,      # 관련 채팅방
            message=warning_message,  # 경고 메시지 저장
            is_read=False  # 아직 읽지 않음 상태로 저장
        )

        print(warning_message)  # 경고 메시지 출력 (이메일 전송, 경고메시지는 프론트엔드에서 주는거)

    def apply_llm_moderation(self):
        """LLM(챗 GPT)로 욕설 감지 자동화"""
        # Chat GPT와 연동해서 자동으로 욕설 감지하는 로직 추가 예정
        pass

    def __str__(self):
        return f'{self.reporter}님이 {self.reported}님 신고함. 사유:{self.content}'
