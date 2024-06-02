from itertools import combinations

def check_divisibility(total, divisors):
    for divisor in map(int, divisors.split(',')):
        if total % divisor != 0:
            return False
    return True

def calculate_sum_and_product(cards):
    card_nums = [int(card) for card in cards]
    total_sum = sum(card_nums)
    total_product = 1
    for num in card_nums:
        total_product *= num
    return total_sum, total_product

def filter_cards(start, end, conditions):
    drawn_cards = range(int(start), int(end) + 1)
    valid_cards = []

    for card_set in combinations(drawn_cards, conditions.get('num_cards', len(drawn_cards))):
        total_sum, total_product = calculate_sum_and_product(card_set)
        if ('sum_divisible_by' in conditions and not check_divisibility(total_sum, conditions['sum_divisible_by'])):
            continue
        if ('product_divisible_by' in conditions and not check_divisibility(total_product, conditions['product_divisible_by'])):
            continue
        valid_cards.append(card_set)
    return valid_cards

def evaluate_conditions(start, end, specific_cards, conditions):
    # If specific_cards is not empty, override start and end to only include these specific cards
    if specific_cards:
        specific_cards_list = specific_cards.split(',')
        start = min(specific_cards_list)
        end = max(specific_cards_list)
    
    valid_cards = filter_cards(start, end, conditions)
    return len(valid_cards), valid_cards

# Example usage within the create_draw_groupbox() if needed
# conditions = {
#     'num_cards': 5,
#     'sum_divisible_by': '10',
#     'product_divisible_by': '20'
# }
# count, valid_sets = evaluate_conditions('1', '50', '', conditions)
# print(f"Valid sets count: {count}")
