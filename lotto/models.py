from django.db import models
from django.contrib.auth.models import User

class LottoRound(models.Model):
    
    round_number = models.PositiveIntegerField(unique=True, verbose_name="회차")
    is_drawn = models.BooleanField(default=False, verbose_name="추첨 완료 여부")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"6/45 로또 제 {self.round_number}회"

class LottoPurchase(models.Model):
    SELECTION_CHOICES = [
        ('AUTO', '자동'),
        ('MANUAL', '수동'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="구매자")
    lotto_round = models.ForeignKey(LottoRound, on_delete=models.CASCADE, verbose_name="회차")
    
    num1 = models.PositiveIntegerField()
    num2 = models.PositiveIntegerField()
    num3 = models.PositiveIntegerField()
    num4 = models.PositiveIntegerField()
    num5 = models.PositiveIntegerField()
    num6 = models.PositiveIntegerField()
    
    selection_type = models.CharField(max_length=6, choices=SELECTION_CHOICES, default='AUTO', verbose_name="선택 유형")
    purchased_at = models.DateTimeField(auto_now_add=True, verbose_name="구매 일시")
    winning_rank = models.CharField(max_length=10, default="추첨 전", verbose_name="당첨 등수") 
    is_won = models.BooleanField(default=False, verbose_name="당첨 여부")

    def get_numbers(self):
        return [self.num1, self.num2, self.num3, self.num4, self.num5, self.num6]

class LottoWinDraw(models.Model):
    lotto_round = models.OneToOneField(LottoRound, on_delete=models.CASCADE, verbose_name="회차")
    
    win1 = models.PositiveIntegerField()
    win2 = models.PositiveIntegerField()
    win3 = models.PositiveIntegerField()
    win4 = models.PositiveIntegerField()
    win5 = models.PositiveIntegerField()
    win6 = models.PositiveIntegerField()
    bonus = models.PositiveIntegerField(verbose_name="보너스 번호")
    drawn_at = models.DateTimeField(auto_now_add=True, verbose_name="추첨 일시")

    def get_win_numbers(self):
        return [self.win1, self.win2, self.win3, self.win4, self.win5, self.win6]