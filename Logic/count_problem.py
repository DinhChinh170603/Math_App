from itertools import product
from concurrent.futures import ProcessPoolExecutor

def generate_numbers(digits, conditions):
    try:
        leng = int(conditions.get('has_k_digits', 1))
    except ValueError:
        leng = 1
    numbers = [''.join(p) for p in product(digits, repeat=leng) if p[0] != '0']
    return numbers

def check_specific_positions(number, positions_str, includes_digits_value=None):
    # Kiểm tra xem các chữ số có ở đúng vị trí cụ thể hay không
    # positions_str: chuỗi vị trí như "1,2,5" hoặc "1,0,5"
    # includes_digits_value: chuỗi chữ số kèm tần suất như "7,7,3"
    # 0 là không yêu cầu vị trí cụ thể
    
    # Nếu một trong các tham số đầu vào trống, bỏ qua điều kiện này
    if not positions_str or not includes_digits_value:
        return True
    
    number_str = str(number)
    
    # Tách danh sách vị trí
    try:
        positions = [int(pos.strip()) for pos in positions_str.split(',') if pos.strip()]
    except ValueError:
        return False
    
    # Tách danh sách chữ số từ includes_digits_value
    digits = [d.strip() for d in includes_digits_value.split(',') if d.strip()]
    
    # Kiểm tra xem có đủ vị trí cho tất cả các chữ số không
    if len(positions) != len(digits):
        return False
    
    # Kiểm tra độ dài số
    max_position = max([p for p in positions if p > 0], default=0)
    if max_position > 0 and len(number_str) < max_position:
        return False
    
    # Tạo mô hình số mẫu theo yêu cầu vị trí
    # Ví dụ với 7,7,3 ở vị trí 1,2,5, mô hình số mẫu sẽ là "77xx3" (với x là bất kỳ)
    template = ['*'] * len(number_str)  # * là ký hiệu đại diện cho bất kỳ chữ số
    
    # Số lần xuất hiện của mỗi chữ số cần đạt được
    required_counts = {}
    for d in digits:
        required_counts[d] = required_counts.get(d, 0) + 1
    
    # Tạo danh sách các chữ số cần ở vị trí cụ thể
    fixed_positions = {}
    for pos, digit in zip(positions, digits):
        if pos > 0:  # Chỉ xử lý vị trí > 0
            pos_idx = pos - 1  # Chuyển sang index bắt đầu từ 0
            fixed_positions[pos_idx] = digit
    
    # Đánh dấu các vị trí cụ thể trong mẫu
    for pos_idx, digit in fixed_positions.items():
        if pos_idx >= len(number_str):
            return False
        template[pos_idx] = digit
    
    # Kiểm tra xem số có phù hợp với mẫu không
    actual_counts = {}
    
    # Kiểm tra từng vị trí trong số
    for i, actual_digit in enumerate(number_str):
        # Nếu vị trí này là vị trí cố định, kiểm tra xem chữ số có đúng không
        if i in fixed_positions:
            if actual_digit != fixed_positions[i]:
                return False
            
        # Đếm số lần xuất hiện của mỗi chữ số
        if actual_digit in required_counts:
            actual_counts[actual_digit] = actual_counts.get(actual_digit, 0) + 1
    
    # Kiểm tra tần suất xuất hiện của các chữ số
    for digit, count in required_counts.items():
        if actual_counts.get(digit, 0) != count:
            return False
    
    return True

def check_conditions(number, conditions):
    condition_funcs = {
        'divisible_by': divisible_by,
        'starts_by': starts_by,
        'not_starts_by': not_starts_by,
        'not_includes_by': not_includes_by,
        'ends_by': ends_by,
        'bigger_than': bigger_than,
        'is_k_digits': is_k_digits,
        'includes_digits': includes_digits,
        'digit_sum_divisible_by': digit_sum_divisible_by,
        'arithmetic_progression': is_arithmetic_progression,
        'geometric_progression': is_geometric_progression,
        'is_even': lambda num, _: num % 2 == 0 if 'is_even' in conditions and conditions['is_even'] else True,
        'is_odd': lambda num, _: num % 2 != 0 if 'is_odd' in conditions and conditions['is_odd'] else True,
        'is_palindrome': lambda num, _: is_palindrome(num) if 'is_palindrome' in conditions and conditions['is_palindrome'] else True,
        'is_prime': lambda num, _: is_prime(num) if 'is_prime' in conditions and conditions['is_prime'] else True,
        'is_square': lambda num, _: is_square(num) if 'is_square' in conditions and conditions['is_square'] else True,
        'is_cube': lambda num, _: is_cube(num) if 'is_cube' in conditions and conditions['is_cube'] else True,
        'all_different': lambda num, _: all_different(num) if 'all_different' in conditions and conditions['all_different'] else True,
        'is_increasing': lambda num, _: is_increasing(num) if 'is_increasing' in conditions and conditions['is_increasing'] else True,
        'is_decreasing': lambda num, _: is_decreasing(num) if 'is_decreasing' in conditions and conditions['is_decreasing'] else True
    }
    
    # Handle special case for specific_positions that needs includes_digits_value
    if 'specific_positions' in conditions and conditions['specific_positions'] is not None:
        includes_digits_value = conditions.get('includes_digits')
        if not check_specific_positions(int(number), conditions['specific_positions'], includes_digits_value):
            return False
    
    # Check all other conditions
    return all(condition_funcs[cond_key](int(number), cond_value) if cond_value is not None else True
               for cond_key, cond_value in conditions.items() 
               if cond_key in condition_funcs and cond_key != 'specific_positions')

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

def is_increasing(number, _=None):
    # Check if digits are in strictly increasing order (e.g., 1289)
    digits = str(number)
    return all(int(digits[i]) < int(digits[i+1]) for i in range(len(digits)-1))

def is_decreasing(number, _=None):
    # Check if digits are in strictly decreasing order (e.g., 9531)
    digits = str(number)
    return all(int(digits[i]) > int(digits[i+1]) for i in range(len(digits)-1))

def digit_sum_divisible_by(number, divisors):
    # Check if sum of digits is divisible by all specified divisors
    digit_sum = sum(int(digit) for digit in str(number))
    return all(digit_sum % int(divisor) == 0 for divisor in divisors.split(','))

def includes_digits(number, digits):
    # Check if specified digits are present with exact frequencies
    # Format: "7,7,3" means the digit 7 appears twice and 3 appears once
    number_str = str(number)
    
    # Handle empty input
    if not digits:
        return True
        
    # Count occurrences of each digit in the input
    digit_counts = {}
    for digit in digits.split(','):
        digit = digit.strip()
        if digit:
            digit_counts[digit] = digit_counts.get(digit, 0) + 1
    
    # Check if each digit appears with the required frequency
    for digit, required_count in digit_counts.items():
        if number_str.count(digit) != required_count:
            return False
            
    return True

# Chức năng kiểm tra tần suất giờ đã được tích hợp vào hàm includes_digits


def is_arithmetic_progression(number, common_difference):
    # Check if digits form an arithmetic progression from left to right
    # e.g., 13579 has common difference 2, 987 has common difference -1
    digits = [int(d) for d in str(number)]
    
    # Need at least 2 digits to check for progression
    if len(digits) < 2:
        return True
    
    # Parse common difference, handle fractions like "1/2" or negative values
    try:
        if '/' in common_difference:
            num, denom = common_difference.split('/')
            d = int(num) / int(denom)
        else:
            d = float(common_difference)
    except (ValueError, ZeroDivisionError):
        return False
    
    # Check if each digit follows the progression pattern
    for i in range(len(digits) - 1):
        # Calculate the expected next digit
        expected_next = digits[i] + d
        # Compare with actual next digit
        if abs(expected_next - digits[i+1]) > 0.00001:  # Use small epsilon for float comparison
            return False
            
    return True


def is_geometric_progression(number, common_ratio):
    # Check if digits form a geometric progression from left to right
    # e.g., 248 has common ratio 2, 8421 has common ratio 1/2
    digits = [int(d) for d in str(number)]
    
    # Need at least 2 digits to check for progression
    if len(digits) < 2:
        return True
    
    # Parse common ratio, handle fractions like "1/2" or negative values
    try:
        if '/' in common_ratio:
            num, denom = common_ratio.split('/')
            r = int(num) / int(denom)
        else:
            r = float(common_ratio)
    except (ValueError, ZeroDivisionError):
        return False
    
    # Check for zeros in the digits since we can't divide by zero
    for i in range(len(digits) - 1):
        if digits[i] == 0 and r != 0:
            # Can't have 0 multiplied by non-zero ratio to get next digit
            return False
            
        # Calculate the expected next digit
        if digits[i] == 0:
            expected_next = 0  # 0 times anything is 0
        else:
            expected_next = digits[i] * r
            
        # Compare with actual next digit (with tolerance for floating point)
        if abs(expected_next - digits[i+1]) > 0.00001:  # Use small epsilon for float comparison
            return False
            
    return True

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