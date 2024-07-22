from itertools import combinations
from multiprocessing import Pool, cpu_count

def count_cards(start, end, tag_list, conditions):
    if tag_list:
        drawn_cards = [int(tag) for tag in tag_list.split(',') if tag.strip().isdigit()]
    else:
        start = int(start)
        end = int(end)
        drawn_cards = list(range(start, end + 1))

    try:
        drawn_cards_len = int(conditions.get('drawn_cards', len(drawn_cards)))
    except ValueError:
        drawn_cards_len = len(drawn_cards)

    valid_combinations = generate_combinations(drawn_cards, drawn_cards_len, conditions)
    return len(valid_combinations), valid_combinations

def generate_combinations(drawn_cards, drawn_cards_len, conditions):
    all_combinations = list(combinations(drawn_cards, drawn_cards_len))
    chunk_size = 10**5  # Điều chỉnh chunk_size để phù hợp với hệ thống của bạn
    comb_chunks = [all_combinations[i:i + chunk_size] for i in range(0, len(all_combinations), chunk_size)]
    
    with Pool(cpu_count() * 2) as pool:
        results = pool.starmap(check_combinations_chunk, [(chunk, conditions) for chunk in comb_chunks])
    
    valid_combinations = [item for sublist in results for item in sublist]
    return valid_combinations

def check_combinations_chunk(comb_chunk, conditions):
    valid_combinations = []
    for combo in comb_chunk:
        if meets_conditions(combo, conditions):
            valid_combinations.append(combo)
    return valid_combinations

def meets_conditions(combo, conditions):
    even_count = 0
    total_sum = 0
    total_product = 1

    for num in combo:
        if num % 2 == 0:
            even_count += 1
        total_sum += num
        total_product *= num

    if 'num_even' in conditions and conditions['num_even'] is not None:
        if even_count != int(conditions['num_even']):
            return False

    if 'sum_divi' in conditions and conditions['sum_divi'] is not None:
        if not check_divisibility(total_sum, conditions['sum_divi']):
            return False

    if 'pro_divi' in conditions and conditions['pro_divi'] is not None:
        if not check_divisibility(total_product, conditions['pro_divi']):
            return False

    return combo

def check_divisibility(total, divisors):
    try:
        divisors = map(int, divisors.split(','))
        return all(total % divisor == 0 for divisor in divisors)
    except ValueError:
        return False