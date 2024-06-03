from itertools import combinations

from networkx import draw

def count_cards(start, end, tag_list, conditions):
    # If 
    if tag_list:
        drawn_cards = [int(tag) for tag in tag_list.split(',') if tag.strip().isdigit()]
        print(f"Tag list: {tag_list}")
    else:
        start = int(start)
        end = int(end)
        drawn_cards = range(start, end + 1)
        print(f"Start: {start}, End: {end}")
    
    valid_cards = filter_cards(drawn_cards, conditions)
    return len(valid_cards), valid_cards

# def check_conditions(cards, conditions):
#     """
#     
#     """
#     if 'drawn_cards' in conditions and conditions['drawn_cards'] is not None and not drawn_cards(cards, conditions['drawn_cards']):
#         return False
#     if 'num_even' in conditions and conditions['num_even'] is not None and not num_even(cards, conditions['num_even']):
#         return False
#     if 'sum_divi' in conditions and conditions['sum_divi'] is not None and not sum_divi(cards, conditions['sum_divi']):
#         return False
#     if 'pro_divi' in conditions and conditions['pro_divi'] is not None and not pro_divi(cards, conditions['pro_divi']):
#         return False
#     return True

def filter_cards(drawn_cards, conditions):
    valid_cards = []
    num_cards = conditions.get('drawn_cards', None)
    num_even = conditions.get('num_even', None)
    sum_divi = conditions.get('sum_divi', None)
    pro_divi = conditions.get('pro_divi', None)

    for card_set in combinations(drawn_cards, num_cards):
        total_sum, total_product = calculate_sum_and_product(card_set)
        if num_even is not None and not check_even_count(card_set, num_even):
            continue
        if sum_divi is not None and not check_divisibility(total_sum, sum_divi):
            continue
        if pro_divi is not None and not check_divisibility(total_product, pro_divi):
            continue
        valid_cards.append(card_set)
    
    return valid_cards

def calculate_sum_and_product(cards):
    card_nums = [int(card) for card in cards]
    total_sum = sum(card_nums)
    total_product = 1
    for num in card_nums:
        total_product *= num
    return total_sum, total_product

def drawn_cards(cards, drawn_cards):
    return len(cards) == drawn_cards

def check_even_count(card_set, num_even):
    even_count = sum(1 for card in card_set if card % 2 == 0)
    return even_count == num_even

def check_divisibility(total, divisors):
    if divisors is None:
        return False

    try:
        divisors = map(int, divisors.split(','))
        return all(total % divisor == 0 for divisor in divisors)
    except ValueError:
        print(f"Error: Invalid input in divisors - {divisors}")
        return False