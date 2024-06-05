from itertools import product

def generate_numbers(digits, conditions):
    leng = conditions.get('has_k_digits', 1)
    numbers = [''.join(p) for p in product(digits, repeat=leng) if p[0] != '0']
    print(f"Generated numbers: {numbers}")
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
        'is_even': lambda num, _: num % 2 == 0,
        'all_different': lambda num, _: all_different(num)
    }
    return all(condition_funcs[cond_key](int(number), cond_value) if cond_value is not None else True
               for cond_key, cond_value in conditions.items() if cond_key in condition_funcs)

def count_numbers(digits, conditions):
    # Generate numbers based on conditions
    numbers = generate_numbers(digits, conditions)
    # Filter numbers based on additional conditions
    valid_numbers = [num for num in numbers if check_conditions(num, conditions)]
    # Return the count of valid numbers and the list of valid numbers
    return len(valid_numbers), valid_numbers

def starts_by(number, starts):
    return any(str(number).startswith(start) for start in starts.split(','))

def not_starts_by(number, not_starts):
    return not any(str(number).startswith(not_start) for not_start in not_starts.split(','))

def not_includes_by(number, k):
    return not all(digit in str(number) for digit in k.split(','))

def divisible_by(number, divisors):
    return all(number % int(divisor) == 0 for divisor in divisors.split(','))

def ends_by(number, ends):
    return number < int(ends)

def bigger_than(number, bigger_than):
    return number > int(bigger_than)

def is_k_digits(number, k):
    return all(digit in str(number) for digit in k.split(','))

def all_different(number, _=None): 
    return len(set(str(number))) == len(str(number))

