import random
from django.shortcuts import render, redirect
from .models import LottoRound, LottoPurchase, LottoWinDraw

def buy_lotto(request):
    
    last_round = LottoRound.objects.order_by('-round_number').first()
    next_round_number = (last_round.round_number + 1) if last_round else 1

    if request.method == "POST":
        selection_type = request.POST.get('selection_type')
        
        if selection_type == 'AUTO':
            numbers = sorted(random.sample(range(1, 46), 6))
        else:
            try:
                numbers = sorted([
                    int(request.POST.get('num_1')), int(request.POST.get('num_2')),
                    int(request.POST.get('num_3')), int(request.POST.get('num_4')),
                    int(request.POST.get('num_5')), int(request.POST.get('num_6'))
                ])
                if len(set(numbers)) != 6 or any(n < 1 or n > 45 for n in numbers):
                    return render(request, 'lotto/buy.html', { 'error': '1부터 45 사이의 중복되지 않은 6개 번호를 입력해주세요.', 'next_round_number': next_round_number})
            except (TypeError, ValueError):
                return render(request, 'lotto/buy.html', { 'error': '6개의 숫자를 모두 올바르게 입력해야 합니다.', 'next_round_number': next_round_number})

        new_round = LottoRound.objects.create(round_number=next_round_number, is_drawn=False)

        LottoPurchase.objects.create(
            lotto_round=new_round,
            num1=numbers[0], num2=numbers[1], num3=numbers[2],
            num4=numbers[3], num5=numbers[4], num6=numbers[5],
            selection_type=selection_type
        )
        
        return redirect(f'/lotto/history/?search_round={new_round.round_number}')
    return render(request, 'lotto/buy.html', {'next_round_number': next_round_number})


def my_lotto_history(request):
    
    search_round_str = request.GET.get('search_round')
    all_rounds = LottoRound.objects.order_by('-round_number')
    
    selected_round = None
    purchase_info = None
    draw_info = None
    rank_result = None
    won = False
    
    if search_round_str:
        try:
            search_round_num = int(search_round_str)
            selected_round = LottoRound.objects.filter(round_number=search_round_num).first()
            
            if selected_round:
                purchase_info = LottoPurchase.objects.filter(lotto_round=selected_round).first()
                draw_info = LottoWinDraw.objects.filter(lotto_round=selected_round).first()
                
                if not draw_info:
                    draw_numbers = random.sample(range(1, 46), 7)
                    win_numbers = sorted(draw_numbers[:6])
                    bonus_number = draw_numbers[6]
                    draw_info = LottoWinDraw.objects.create(
                        lotto_round=selected_round,
                        win1=win_numbers[0], win2=win_numbers[1], win3=win_numbers[2],
                        win4=win_numbers[3], win5=win_numbers[4], win6=win_numbers[5],
                        bonus=bonus_number
                    )
                    selected_round.is_drawn = True
                    selected_round.save()

                if purchase_info:
                    my_nums = set(purchase_info.get_numbers())
                    win_nums = set(draw_info.get_win_numbers())
                    matched = len(my_nums.intersection(win_nums))
                    
                    if matched == 6:
                        rank_result = "1등 (6개 일치)"
                        won = True
                    elif matched == 5 and draw_info.bonus in my_nums:
                        rank_result = "2등 (5개 + 보너스 일치)"
                        won = True
                    elif matched == 5:
                        rank_result = "3등 (5개 일치)"
                        won = True
                    elif matched == 4:
                        rank_result = "4등 (4개 일치)"
                        won = True
                    elif matched == 3:
                        rank_result = "5등 (3개 일치)"
                        won = True
                    else:
                        rank_result = "꽝"
                    purchase_info.winning_rank = rank_result
                    purchase_info.is_won = won
                    purchase_info.save()
        except ValueError:
            pass

    return render(request, 'lotto/history.html', {
        'all_rounds': all_rounds,
        'selected_round': selected_round,
        'purchase_info': purchase_info,
        'draw_info': draw_info,
        'rank_result': rank_result,
        'search_round': search_round_str
    })