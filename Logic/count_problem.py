from itertools import product
from concurrent.futures import ProcessPoolExecutor

def generate_numbers(digits, conditions):
    try:
        leng = int(conditions.get('has_k_digits', 1))
    except ValueError:
        leng = 1
    numbers = [''.join(p) for p in product(digits, repeat=leng) if p[0] != '0']
    return numbers

def check_conditions(number, conditions):
    condition_funcs = {
        'divisible_by': divisible_by,
        'starts_by': starts_by,
        'not_starts_by': not_starts_by,
        'not_includes_by': not_includes_by,
        'ends_by': ends_by,
        'bigger_than': bigger_than,
        'is_k_digits': is_k_digits,
        'is_even': lambda num, _: num % 2 == 0 if 'is_even' in conditions and conditions['is_even'] else True,
        'is_odd': lambda num, _: num % 2 != 0 if 'is_odd' in conditions and conditions['is_odd'] else True,
        'is_palindrome': lambda num, _: is_palindrome(num) if 'is_palindrome' in conditions and conditions['is_palindrome'] else True,
        'is_prime': lambda num, _: is_prime(num) if 'is_prime' in conditions and conditions['is_prime'] else True,
        'is_square': lambda num, _: is_square(num) if 'is_square' in conditions and conditions['is_square'] else True,
        'is_cube': lambda num, _: is_cube(num) if 'is_cube' in conditions and conditions['is_cube'] else True,
        'all_different': lambda num, _: all_different(num) if 'all_different' in conditions and conditions['all_different'] else True
    }
    return all(condition_funcs[cond_key](int(number), cond_value) if cond_value is not None else True
               for cond_key, cond_value in conditions.items() if cond_key in condition_funcs)

def starts_by(number, starts):
    return any(str(number).startswith(start) for start in starts.split(','))

def not_starts_by(number, not_starts):
    return not any(str(number).startswith(not_start) for not_start in not_starts.split(','))

def not_includes_by(number, k):
    return not any(digit in str(number) for digit in k.split(','))

def divisible_by(number, divisors):
    return all(number % int(divisor) == 0 for divisor in divisors.split(','))

def ends_by(number, ends):
    return number < int(ends)

def bigger_than(number, bigger_than):
    return number > int(bigger_than)

def is_k_digits(number, k):
    return all(digit in str(number) for digit in k.split(','))

def is_palindrome(number, _=None):
    s = str(number)
    return s == s[::-1]

def is_prime(number, _=None):
    if number <= 1:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True

def is_square(number, _=None):
    return int(number**0.5) ** 2 == number

def is_cube(number, _=None):
    return int(round(number**(1/3))) ** 3 == number

def all_different(number, _=None): 
    return len(set(str(number))) == len(str(number))

def process_chunk(chunk, conditions):
    return [num for num in chunk if check_conditions(num, conditions)]

def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]

def count_numbers(digits, conditions):
    numbers = generate_numbers(digits, conditions)
    num_chunks = min(64, len(numbers))  # Number of chunks/processes to create
    chunks = chunkify(numbers, num_chunks)
    
    with ProcessPoolExecutor() as executor:
        results = executor.map(process_chunk, chunks, [conditions]*num_chunks)
    
    valid_numbers = [num for sublist in results for num in sublist]
    valid_numbers.sort()
    return len(valid_numbers), valid_numbers