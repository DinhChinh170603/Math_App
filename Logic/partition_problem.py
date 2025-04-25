from itertools import permutations
from collections import Counter
import math
import os
import datetime

def parse_partition_input(input_data):
    """
    Parse input string to a list of counts for types.
    Example: "1,4,6" -> [1, 4, 6]
    """
    try:
        counts = list(map(int, input_data.split(',')))
        return counts
    except ValueError:
        raise ValueError("Đầu vào không hợp lệ. Vui lòng nhập các số cách nhau bởi dấu phẩy.")

def parse_labels_input(input_data):
    """
    Parse input string to a list of labels.
    Example: "Nam,Nữ,Trẻ em" -> ["Nam", "Nữ", "Trẻ em"]
    """
    if not input_data or input_data.strip() == "":
        return None
    
    labels = [label.strip() for label in input_data.split(',')]
    return labels

def generate_elements(counts, custom_labels=None):
    """
    Generate a list of elements based on counts and optional custom labels.
    Example with default labels: [1, 4, 6] -> ["A", "B", "B", "B", "B", "C", "C", "C", "C", "C", "C"]
    Example with custom labels: [5, 22], ["Nam", "Nữ"] -> ["Nam", "Nam", "Nam", "Nam", "Nam", "Nữ", "Nữ", ...]
    """
    if custom_labels and len(custom_labels) != len(counts):
        raise ValueError("Số lượng nhãn phải bằng số lượng loại.")
        
    # Use custom labels if provided, otherwise use default A, B, C...
    labels = custom_labels if custom_labels else [chr(65 + i) for i in range(len(counts))]
    elements = [label for label, count in zip(labels, counts) for _ in range(count)]
    return elements

def calculate_total_permutations(elements):
    """Calculate the total number of possible permutations"""
    counter = Counter(elements)
    total = math.factorial(len(elements))
    for count in counter.values():
        total //= math.factorial(count)
    return total

def is_valid(perm):
    """
    Check if a permutation is valid for row arrangement (no two adjacent elements are the same).
    """
    for i in range(1, len(perm)):
        if perm[i] == perm[i - 1]:
            return False
    return True

def is_valid_circular(perm):
    """
    Check if a permutation is valid for circular arrangement (no two adjacent elements are the same).
    """
    n = len(perm)
    if n <= 1:
        return True
        
    for i in range(n):
        if perm[i] == perm[(i + 1) % n]:
            return False
    return True

def generate_row_permutations_chunked(elements, chunk_size=1000, progress_callback=None, result_file=None):
    """
    Generate valid row permutations in chunks to avoid freezing the UI.
    Returns a generator that yields chunks of valid permutations.
    """
    total_perms = calculate_total_permutations(elements)
    
    # Generate permutations in chunks
    perm_generator = permutations(elements)
    chunk = []
    count = 0
    total_processed = 0
    
    # Open file if provided
    f = None
    if result_file:
        os.makedirs(os.path.dirname(result_file), exist_ok=True)
        f = open(result_file, 'w', encoding='utf-8')
        f.write(f"Permutations generated on {datetime.datetime.now()}\n\n")
    
    try:
        for perm in perm_generator:
            total_processed += 1
            if is_valid(perm):
                if f:
                    # Write to file
                    f.write(f"{'|'.join(perm)}\n")
                
                chunk.append(perm)
                count += 1
                
                if len(chunk) >= chunk_size:
                    if progress_callback:
                        progress = min(99, int((total_processed * 100) / total_perms))
                        progress_callback.emit(progress, count)
                    
                    # For large result sets, we yield but clear the chunk to save memory
                    if f:
                        chunk.clear()
                    else:
                        yield chunk
                        chunk = []
        
        if chunk or f:  # Yield any remaining items or finalize file
            if progress_callback:
                progress_callback.emit(100, count)
            
            if f:
                f.close()
                yield [] # Empty chunk to signal completion
            else:
                yield chunk
                
    except Exception as e:
        print(f"Error in chunked generation: {e}")
        if f:
            f.close()
        if chunk:
            yield chunk

def generate_circle_permutations_chunked(elements, chunk_size=1000, progress_callback=None, result_file=None):
    """
    Generate valid circular permutations in chunks to avoid freezing the UI.
    """
    total_perms = calculate_total_permutations(elements)
    
    # We can fix the first element and permute the rest to reduce computation
    if len(elements) <= 1:
        if elements:
            yield elements
        return
        
    first_element = elements[0]
    rest_elements = elements[1:]
    
    # Open file if provided
    f = None
    if result_file:
        os.makedirs(os.path.dirname(result_file), exist_ok=True)
        f = open(result_file, 'w', encoding='utf-8')
        f.write(f"Circular permutations generated on {datetime.datetime.now()}\n\n")
    
    # Generate permutations in chunks
    perm_generator = permutations(rest_elements)
    chunk = []
    count = 0
    total_processed = 0
    
    try:
        for perm in perm_generator:
            total_processed += 1
            full_perm = tuple([first_element] + list(perm))
            
            if is_valid_circular(full_perm):
                if f:
                    # Write to file
                    f.write(f"{'-'.join(full_perm)}\n")
                
                chunk.append(full_perm)
                count += 1
                
                if len(chunk) >= chunk_size:
                    if progress_callback:
                        progress = min(99, int((total_processed * 100) / (total_perms / len(elements))))
                        progress_callback.emit(progress, count)
                    
                    # For large result sets, we yield but clear the chunk to save memory
                    if f:
                        chunk.clear()
                    else:
                        yield chunk
                        chunk = []
        
        if chunk or f:  # Yield any remaining items or finalize file
            if progress_callback:
                progress_callback.emit(100, count)
            
            if f:
                f.close()
                yield [] # Empty chunk to signal completion
            else:
                yield chunk
                
    except Exception as e:
        print(f"Error in chunked generation: {e}")
        if f:
            f.close()
        if chunk:
            yield chunk

def get_results_directory():
    """Get the directory where results will be saved"""
    base_dir = os.path.join(os.path.expanduser("~"), "TMQ-Math-Results")
    os.makedirs(base_dir, exist_ok=True)
    return base_dir

def get_result_file_path(is_circle, labels=None):
    """Generate a file path for results based on current time and parameters"""
    results_dir = get_results_directory()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create descriptive filename
    if labels:
        label_part = "_".join(labels)
        label_part = label_part[:30]  # Limit length
        filename = f"{'circle' if is_circle else 'row'}_permutations_{label_part}_{timestamp}.txt"
    else:
        filename = f"{'circle' if is_circle else 'row'}_permutations_{timestamp}.txt"
    
    return os.path.join(results_dir, filename)
