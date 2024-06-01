from itertools import product

# def parse_input(input_string):
#     """Chuyển chuỗi đầu vào thành danh sách các số."""
#     return [num.strip() for num in input_string.split(',')]

def generate_numbers(digits, conditions):
    leng = conditions['has_k_digits']
    if 'has_k_digits' in conditions and conditions['has_k_digits'] is None:
        leng = 1
    """Tạo tất cả các số có độ dài 'length' từ 'digits', tránh số bắt đầu bằng '0'."""
    numbers = [''.join(p) for p in product(digits, repeat=leng) if p[0] != '0']
    print(f"Generated numbers: {numbers}")
    return numbers

def check_conditions(number, conditions):
    number = int(number)
    """
    Kiểm tra xem số đưa vào có thỏa mãn tất cả các điều kiện không.
    """
    if 'has_k_digits' in conditions and conditions['has_k_digits'] is not None and not has_k_digits(number, conditions['has_k_digits']):
        return False
    if 'divisible_by' in conditions and conditions['divisible_by'] is not None and not divisible_by(number, conditions['divisible_by']):
        return False
    if 'starts_by' in conditions and conditions['starts_by'] is not None and not starts_by(number, conditions['starts_by']):
        return False
    if 'not_starts_by' in conditions and conditions['not_starts_by'] is not None and not not_starts_by(number, conditions['not_starts_by']):
        return False
    if 'not_includes_by' in conditions and conditions['not_includes_by'] is not None and not not_includes_by(number, conditions['not_includes_by']):
        return False
    if 'ends_by' in conditions and conditions['ends_by'] is not None and not ends_by(number, conditions['ends_by']):
        return False
    if 'bigger_than' in conditions and conditions['bigger_than'] is not None and not bigger_than(number, conditions['bigger_than']):
        return False
    if 'is_k_digits' in conditions and conditions['is_k_digits'] is not None and not is_k_digits(number, conditions['is_k_digits']):
        return False
    if 'is_even' in conditions and conditions['is_even'] and number % 2 != 0:
        return False
    if 'is_odd' in conditions and conditions['is_odd'] and number % 2 == 0:
        return False
    if 'all_different' in conditions and conditions['all_different'] and len(set(str(number))) != len(str(number)):
        return False
    return True

def count_numbers(input_digits, conditions):
    """
    Đếm số lượng số và trả ra kết quả thỏa mãn dựa vào các điều kiện đã cho.
    """
    numbers = generate_numbers(input_digits, conditions)
    filtered_numbers = [num for num in numbers if check_conditions(num, conditions)]
    return len(filtered_numbers), filtered_numbers  # Trả về cả số lượng lẫn danh sách

def has_k_digits(number, k):
    """Kiểm tra xem số có đúng k chữ số không."""
    k = int(k)
    return len(str(number)) == k

def starts_by(number, starts):
    """Kiểm tra xem số đầu bằng 'start'."""
    try:
        starts = starts.split(',')
        number = str(number)
        return any(number.startswith(start) for start in starts)
    except ValueError:
        print(f"Error: Invalid input in starts - {starts}")
        return False
    
def not_starts_by(number, not_starts):
    """Kiểm tra xem số đầu khác 'not_start'."""
    try:
        not_starts = not_starts.split(',')
        number = str(number)
        return not any(number.startswith(not_start) for not_start in not_starts)
    except ValueError:
        print(f"Error: Invalid input in not_starts - {not_starts}")
        return False
    
def not_includes_by(number, k):
    try:
        number_str = str(number)
        digit_list = k.split(',')
        return not all(digit in number_str for digit in digit_list)
    except ValueError:
        print(f"Error: Invalid input in k - {k}")
        return False


def divisible_by(number, divisors):
    """Kiểm tra xem số có chia hết cho divisor không."""
    # Nếu divisor là 1 chuỗi
    try:
        divisors = map(int, divisors.split(','))  # Chuyển đổi chuỗi nhập vào thành danh sách các số
        return all(number % divisor == 0 for divisor in divisors)
    except ValueError:
        print(f"Error: Invalid input in divisors - {divisors}")
        return False
    
def ends_by(number, ends):
    """Kiểm tra xem số đó nhỏ hơn 'end'."""
    try:
        return number < int(ends)
    except ValueError:
        print(f"Error: Invalid input in ends - {ends}")
        return False
    
def bigger_than(number, bigger_than):
    """Kiểm tra xem số đó lớn hơn 'bigger_than'."""
    try:
        return number > int(bigger_than)
    except ValueError:
        print(f"Error: Invalid input in bigger_than - {bigger_than}")
        return False
    
def is_k_digits(number, k):
    """Kiểm tra xem số có chứa các chữ số k không."""
    try:
        number_str = str(number)
        digit_list = k.split(',')
        return all(digit in number_str for digit in digit_list)
    except ValueError:
        print(f"Error: Invalid input in k - {k}")
        return False

