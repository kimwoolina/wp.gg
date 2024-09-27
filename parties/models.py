from django.db import models
from users.models import User
# Create your models here.
class Parties(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rank = models.CharField()
    server = models.CharField()
    language = models.CharField()
    age = models.selection_field()
    gender = models.selection_field()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_rank = models.BooleanField(default=False)
    
    # User1
    top1 = models.ForeignKey(User, on_delete=models.CASCADE)
    jungle1 = models.ForeignKey(User, on_delete=models.CASCADE)
    mid1 = models.ForeignKey(User, on_delete=models.CASCADE)
    support1 = models.ForeignKey(User, on_delete=models.CASCADE)
    adc1 = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # User2
    top2 = models.ForeignKey(User, on_delete=models.CASCADE)
    jungle2 = models.ForeignKey(User, on_delete=models.CASCADE)
    mid2 = models.ForeignKey(User, on_delete=models.CASCADE)
    support2 = models.ForeignKey(User, on_delete=models.CASCADE)
    adc2 = models.ForeignKey(User, on_delete=models.CASCADE)