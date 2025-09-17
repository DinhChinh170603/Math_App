from itertools import product
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
import os
from typing import Generator, List, Tuple, Dict, Any
import gc

def generate_numbers_optimized(digits: str, conditions: Dict[str, Any]) -> Generator[int, None, None]:
    """Memory-efficient generator that yields numbers one at a time instead of creating a list."""
    try:
        leng = int(conditions.get('has_k_digits', 1))
    except ValueError:
        leng = 1
    
    allow_leading_zeros = conditions.get('allow_leading_zeros', False)
    
    # Use generator to avoid storing all combinations in memory
    if allow_leading_zeros:
        for p in product(digits, repeat=leng):
            yield int(''.join(p))
    else:
        for p in product(digits, repeat=leng):
            if p[0] != '0':  # Skip numbers with leading zeros
                yield int(''.join(p))

def generate_numbers(digits, conditions):
    """Legacy function for backward compatibility - converts generator to list."""
    return list(generate_numbers_optimized(digits, conditions))

def check_specific_positions(number, positions_str, includes_digits_value=None, allow_leading_zeros=False):
    
    if not positions_str or not includes_digits_value:
        return True
    
    # Get the number as string, preserving leading zeros if allow_leading_zeros is True
    if allow_leading_zeros:
        # For numbers with leading zeros, we need to preserve the original string format
        # This is a special case for positions counting when allow_leading_zeros is True
        number_str = str(number)
        
        # If it's just a single digit 0, we return it as is
        if number == 0:
            number_str = '0'
    else:
        # Regular case - use int to remove leading zeros
        number_str = str(number)
    
    try:
        positions = [int(pos.strip()) for pos in positions_str.split(',') if pos.strip()]
    except ValueError:
        return False
    
    digits = [d.strip() for d in includes_digits_value.split(',') if d.strip()]
    
    if len(positions) != len(digits):
        return False
    
    max_position = max([p for p in positions if p > 0], default=0)
    if max_position > 0 and len(number_str) < max_position:
        return False
    
    template = ['*'] * len(number_str)  
    
    required_counts = {}
    for d in digits:
        required_counts[d] = required_counts.get(d, 0) + 1
    
    fixed_positions = {}
    for pos, digit in zip(positions, digits):
        if pos > 0: 
            pos_idx = pos - 1 
            fixed_positions[pos_idx] = digit
    
    for pos_idx, digit in fixed_positions.items():
        if pos_idx >= len(number_str):
            return False
        template[pos_idx] = digit
    
    actual_counts = {}
    
    for i, actual_digit in enumerate(number_str):
        if i in fixed_positions:
            if actual_digit != fixed_positions[i]:
                return False
            
        if actual_digit in required_counts:
            actual_counts[actual_digit] = actual_counts.get(actual_digit, 0) + 1
    
    for digit, count in required_counts.items():
        if actual_counts.get(digit, 0) != count:
            return False
    
    return True

def check_remainder(number, remainder_str):
    try:
        if '%' in remainder_str and '=' in remainder_str:
            parts = remainder_str.replace('%', '').split('=')
            if len(parts) != 2:
                return False
                
            a = int(parts[0].strip())
            b = int(parts[1].strip())
            
            if a <= 0:
                return False 
                
            return number % a == b
            
        return False 
    except (ValueError, IndexError):
        return False 

def check_conditions(number, conditions):
    condition_funcs = {
        'divisible_by': divisible_by,
        'digit_sum_compare': digit_sum_comparison,
        'not_divisible_by': not_divisible_by,
        'starts_by': starts_by,
        'not_starts_by': not_starts_by,
        'not_includes_by': not_includes_by,
        'ends_by': ends_by,
        'bigger_than': bigger_than,
        'is_k_digits': is_k_digits,
        'includes_digits': includes_digits,
        'digit_sum_divisible_by': digit_sum_divisible_by,
        'remainder': check_remainder,
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
    
    if 'specific_positions' in conditions and conditions['specific_positions'] is not None:
        includes_digits_value = conditions.get('includes_digits')
        allow_leading_zeros = conditions.get('allow_leading_zeros', False)
        
        # When allow_leading_zeros is True, we need to preserve the original number string
        # to correctly evaluate positions with leading zeros
        if not check_specific_positions(number, conditions['specific_positions'], includes_digits_value, allow_leading_zeros):
            return False
    
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
    return all(int(number) % int(divisor) == 0 for divisor in divisors.split(','))

def not_divisible_by(number, divisors):
    return all(int(number) % int(divisor) != 0 for divisor in divisors.split(','))

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
    digits = str(number)
    return all(int(digits[i]) < int(digits[i+1]) for i in range(len(digits)-1))

def is_decreasing(number, _=None):
    digits = str(number)
    return all(int(digits[i]) > int(digits[i+1]) for i in range(len(digits)-1))

def digit_sum_divisible_by(number, divisors):
    digit_sum = sum(int(digit) for digit in str(number))
    return all(digit_sum % int(divisor) == 0 for divisor in divisors.split(','))

def digit_sum_comparison(number, comparison_str):
    
    digit_sum = sum(int(digit) for digit in str(number))
    
    if not comparison_str or comparison_str.strip() == "":
        return True
    
    conditions = comparison_str.split(',')
    
    for condition in conditions:
        condition = condition.strip()
        if not condition:
            continue
            
        operators = ["<=", ">=", "=", "!=", "<", ">"]
        found_operator = None
        value = None
        
        for op in operators:
            if op in condition:
                found_operator = op
                value_str = condition.replace(op, "").strip()
                try:
                    value = int(value_str)
                    break
                except ValueError:
                    return False
        
        if found_operator is None or value is None:
            return False
        
        result = False
        if found_operator == "<":
            result = digit_sum < value
        elif found_operator == ">":
            result = digit_sum > value
        elif found_operator == "=":
            result = digit_sum == value
        elif found_operator == "!=":
            result = digit_sum != value
        elif found_operator == "<=":
            result = digit_sum <= value
        elif found_operator == ">=":
            result = digit_sum >= value
        
        if not result:
            return False
    
    return True

def includes_digits(number, digits):
    number_str = str(number)
    
    if not digits:
        return True
        
    digit_counts = {}
    for digit in digits.split(','):
        digit = digit.strip()
        if digit:
            digit_counts[digit] = digit_counts.get(digit, 0) + 1
    
    for digit, required_count in digit_counts.items():
        if number_str.count(digit) != required_count:
            return False
            
    return True


def is_arithmetic_progression(number, common_difference):
    digits = [int(d) for d in str(number)]
    
    if len(digits) < 2:
        return True
    
    try:
        if '/' in common_difference:
            num, denom = common_difference.split('/')
            d = int(num) / int(denom)
        else:
            d = float(common_difference)
    except (ValueError, ZeroDivisionError):
        return False
    
    for i in range(len(digits) - 1):
        expected_next = digits[i] + d
        if abs(expected_next - digits[i+1]) > 0.00001: 
            return False
            
    return True


def is_geometric_progression(number, common_ratio):
    digits = [int(d) for d in str(number)]
    
    if len(digits) < 2:
        return True
    
    try:
        if '/' in common_ratio:
            num, denom = common_ratio.split('/')
            r = int(num) / int(denom)
        else:
            r = float(common_ratio)
    except (ValueError, ZeroDivisionError):
        return False
    
    for i in range(len(digits) - 1):
        if digits[i] == 0 and r != 0:
            return False
            
        if digits[i] == 0:
            expected_next = 0 
        else:
            expected_next = digits[i] * r
            
        if abs(expected_next - digits[i+1]) > 0.00001: 
            return False
            
    return True

def process_batch_optimized(start_range: int, end_range: int, digits: str, conditions: Dict[str, Any], 
                           batch_size: int = 10000) -> List[int]:
    """Process a range of numbers in small batches to avoid memory issues."""
    valid_numbers = []
    current_batch = []
    
    # Generate numbers in the specified range
    try:
        leng = int(conditions.get('has_k_digits', 1))
    except ValueError:
        leng = 1
    
    allow_leading_zeros = conditions.get('allow_leading_zeros', False)
    
    # Create range-based generator for this specific range
    for p in product(digits, repeat=leng):
        if not allow_leading_zeros and p[0] == '0':
            continue
            
        num = int(''.join(p))
        if start_range <= num <= end_range:
            current_batch.append(num)
            
            # Process batch when it reaches batch_size
            if len(current_batch) >= batch_size:
                valid_numbers.extend([n for n in current_batch if check_conditions(n, conditions)])
                current_batch = []
                gc.collect()  # Force garbage collection
    
    # Process remaining numbers in the last batch
    if current_batch:
        valid_numbers.extend([n for n in current_batch if check_conditions(n, conditions)])
    
    return valid_numbers

def save_results_to_files(valid_numbers: List[int], output_dir: str = "results") -> List[str]:
    """Split large result sets into 4 JSON files to avoid memory issues."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Clear existing result files
    for i in range(1, 5):
        file_path = os.path.join(output_dir, f"results_part_{i}.json")
        if os.path.exists(file_path):
            os.remove(file_path)
    
    if len(valid_numbers) <= 50000:  # Small result set - return as usual
        return []
    
    # Split into 4 parts for large result sets
    chunk_size = len(valid_numbers) // 4
    file_paths = []
    
    for i in range(4):
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size if i < 3 else len(valid_numbers)
        chunk = valid_numbers[start_idx:end_idx]
        
        file_path = os.path.join(output_dir, f"results_part_{i+1}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({
                "count": len(chunk),
                "min_value": min(chunk) if chunk else 0,
                "max_value": max(chunk) if chunk else 0,
                "numbers": chunk
            }, f, ensure_ascii=False, indent=2)
        
        file_paths.append(file_path)
    
    return file_paths

def count_numbers_optimized(digits: str, conditions: Dict[str, Any], 
                          max_memory_results: int = 50000, progress_callback=None) -> Tuple[int, List[int], List[str]]:
    """Optimized counting function with memory management and file output."""
    try:
        leng = int(conditions.get('has_k_digits', 1))
    except ValueError:
        leng = 1
    
    # Calculate total possible combinations to estimate memory usage
    total_combinations = len(digits) ** leng
    if not conditions.get('allow_leading_zeros', False):
        # Subtract combinations starting with 0
        total_combinations -= len(digits) ** (leng - 1) if leng > 1 else 0
    
    progress_msg = f"Bắt đầu xử lý {total_combinations:,} tổ hợp..."
    print(progress_msg)
    if progress_callback:
        progress_callback(progress_msg)
    
    valid_numbers = []
    processed_count = 0
    batch_size = min(10000, max(1000, total_combinations // 100))  # Adaptive batch size
    
    # Use generator to process numbers in batches
    current_batch = []
    for num in generate_numbers_optimized(digits, conditions):
        current_batch.append(num)
        processed_count += 1
        
        # Process batch when it reaches batch_size
        if len(current_batch) >= batch_size:
            valid_batch = [n for n in current_batch if check_conditions(n, conditions)]
            valid_numbers.extend(valid_batch)
            current_batch = []
            gc.collect()  # Force garbage collection
            
            # Progress indicator
            if processed_count % 50000 == 0:
                progress_msg = f"Đã xử lý {processed_count:,}/{total_combinations:,} số, tìm thấy {len(valid_numbers):,} số hợp lệ"
                print(progress_msg)
                if progress_callback:
                    progress_callback(progress_msg)
    
    # Process remaining numbers in the last batch
    if current_batch:
        valid_batch = [n for n in current_batch if check_conditions(n, conditions)]
        valid_numbers.extend(valid_batch)
    
    # Final progress update
    progress_msg = f"Hoàn thành! Đã xử lý {processed_count:,} số, tìm thấy {len(valid_numbers):,} số hợp lệ"
    print(progress_msg)
    if progress_callback:
        progress_callback(progress_msg)
    
    valid_numbers.sort()
    
    # Handle large result sets by saving to files
    file_paths = []
    if len(valid_numbers) > max_memory_results:
        progress_msg = f"Kết quả lớn ({len(valid_numbers):,} số). Đang lưu vào file..."
        print(progress_msg)
        if progress_callback:
            progress_callback(progress_msg)
        
        file_paths = save_results_to_files(valid_numbers)
        # Keep only a sample for UI display
        display_numbers = valid_numbers[:max_memory_results]
        return len(valid_numbers), display_numbers, file_paths
    
    return len(valid_numbers), valid_numbers, file_paths

def process_chunk(chunk, conditions):
    """Legacy function for backward compatibility."""
    return [num for num in chunk if check_conditions(num, conditions)]

def chunkify(lst, n):
    """Legacy function for backward compatibility."""
    return [lst[i::n] for i in range(n)]

def count_numbers(digits, conditions):
    """Legacy function - now uses optimized version for better performance."""
    total_count, valid_numbers, file_paths = count_numbers_optimized(digits, conditions)
    
    # If files were created, inform about them
    if file_paths:
        print(f"Results saved to {len(file_paths)} files in 'results' directory")
        print("File paths:", file_paths)
    
    return total_count, valid_numbers