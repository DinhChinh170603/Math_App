from itertools import product

def parse_input(input_string):
    """Chuyển chuỗi đầu vào thành danh sách các số."""
    return [num.strip() for num in input_string.split(',')]

def generate_numbers(digits, length):
    """Tạo tất cả các số có độ dài 'length' từ 'digits', tránh số bắt đầu bằng '0'."""
    numbers = [''.join(p) for p in product(digits, repeat=length) if p[0] != '0']
    print(f"Generated numbers: {numbers}")
    return numbers

def calculate_conditions(numbers, conditions):
    """Kiểm tra các số dựa trên điều kiện đã cho và trả về số lượng số thỏa mãn."""
    condition_funcs = {
        'has_k_digits': lambda num, k: len(str(num)) == k,
        'divisible_by': lambda num, div: int(num) % int(div) == 0,
    }
    
    count = 0
    for number in numbers:
        if all(condition_funcs[cond](number, val) for cond, val in conditions.items() if cond in condition_funcs):
            count += 1
    return count

def count_numbers(input_digits, num_length, conditions):
    """Tạo số từ các chữ số đầu vào và kiểm tra chúng dựa trên điều kiện."""
    numbers = generate_numbers(input_digits, num_length)
    print(f"Initial numbers count: {len(numbers)}")

    if conditions.get('divisible_by'):
        numbers = [num for num in numbers if int(num) % conditions['divisible_by'] == 0]
        print(f"Numbers after divisibility filter: {len(numbers)}")

    return len(numbers)

