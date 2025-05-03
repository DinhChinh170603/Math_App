import asyncio
from functools import partial
from itertools import permutations
from collections import Counter
import math
import os
import datetime

from Logic.partition_problem import (
    is_valid, is_valid_circular, calculate_total_permutations,
    get_result_file_path
)

async def async_generate_permutations(elements, is_circle=False, chunk_size=1000, progress_callback=None, result_file=None):
    """
    Generate valid permutations asynchronously, yielding control back to the event loop regularly.
    This prevents UI freezing while processing extremely large datasets.
    """
    total_perms = calculate_total_permutations(elements)
    
    # Log start of calculation
    print(f"Starting permutation calculation for {len(elements)} elements, total possible: {total_perms:,}")
    
    # Open file if provided
    f = None
    if result_file:
        os.makedirs(os.path.dirname(result_file), exist_ok=True)
        f = open(result_file, 'w', encoding='utf-8')
        perm_type = "Circular" if is_circle else "Row"
        f.write(f"{perm_type} permutations generated on {datetime.datetime.now()}\n\n")
    
    try:
        # Setup based on permutation type
        if is_circle and len(elements) > 1:
            # For circular permutations, we can fix the first element and permute the rest
            first_element = elements[0]
            rest_elements = elements[1:]
            permutation_input = rest_elements
            validation_func = is_valid_circular
            format_func = lambda perm: tuple([first_element] + list(perm))
            separator = '-'
        else:
            # For row permutations, we process all elements
            permutation_input = elements
            validation_func = is_valid
            format_func = lambda perm: perm
            separator = '|'
        
        # Initialize counters
        chunk = []
        count = 0
        total_processed = 0
        last_yield_time = datetime.datetime.now()
        start_time = datetime.datetime.now()
        
        # Use a loop to manually control iteration and allow async processing
        perm_iterator = permutations(permutation_input)
        
        while True:
            # Process a mini-batch before yielding control
            mini_batch_size = 10000  # Number of permutations to check before yielding control
            mini_batch_found = 0
            
            for _ in range(mini_batch_size):
                try:
                    perm = next(perm_iterator)
                except StopIteration:
                    print(f"Completed all permutations. Total processed: {total_processed:,}, valid found: {count:,}")
                    break
                
                total_processed += 1
                
                # Format the permutation based on type
                full_perm = format_func(perm)
                
                # Check if permutation is valid
                if validation_func(full_perm):
                    mini_batch_found += 1
                    if f:
                        # Write to file
                        f.write(f"{separator.join(full_perm)}\n")
                    else:
                        chunk.append(full_perm)
                    count += 1
                    
                    # If chunk is full, yield it or clear it
                    if len(chunk) >= chunk_size:
                        if progress_callback:
                            progress = min(99, int((total_processed * 100) / total_perms))
                            progress_callback(progress, count)
                        
                        # For large result sets, clear the chunk to save memory
                        if not f:
                            yield chunk
                            chunk = []
            
            # Update progress more frequently for larger datasets
            current_time = datetime.datetime.now()
            if (current_time - last_yield_time).total_seconds() > 0.2:  # Update every 200ms for more responsive UI
                elapsed = (current_time - start_time).total_seconds()
                if total_processed > 0 and progress_callback:
                    progress = min(99, int((total_processed * 100) / total_perms))
                    # Every minute, also log progress to console
                    if (current_time - start_time).total_seconds() % 60 < 0.2:
                        print(f"Progress: {progress}%, processed: {total_processed:,}/{total_perms:,}, found: {count:,}")
                    progress_callback(progress, count)
                last_yield_time = current_time

            # No permutations found in this mini-batch, we're possibly done
            if mini_batch_found == 0 and total_processed >= total_perms:
                break
                
            # Yield control back to the event loop
            await asyncio.sleep(0)
            
            # Break if we've processed what we expect to be all permutations
            if total_processed >= total_perms:
                break
        
        # Final yield of remaining items
        if chunk or f:
            if progress_callback:
                progress_callback(100, count)
            
            if f:
                f.close()
                print(f"Results written to file: {result_file}")
                yield []  # Empty chunk to signal completion
            else:
                yield chunk
                
    except Exception as e:
        print(f"Error in async permutation generation: {e}")
        import traceback
        traceback.print_exc()
        if f:
            f.close()
        if chunk:
            yield chunk

async def run_partition_calculation(counts, elements, is_circle=False, 
                                   progress_callback=None, result_file=None):
    """
    Run the partition calculation asynchronously.
    Returns total count and a sample of results.
    """
    results = []
    total_count = 0
    
    try:
        # Simple check to see if solution is possible
        counter = Counter(elements)
        element_counts = list(counter.values())
        max_count = max(element_counts)
        total_elements = sum(element_counts)
        
        # Log input information
        print(f"Starting partition calculation: {counts}, circle: {is_circle}")
        print(f"Elements distribution: {dict(counter)}")
        
        # For row arrangements, max count of any element type should be <= (total+1)/2
        # For circular arrangements with >2 elements, max count should be <= total/2
        if ((not is_circle and max_count > (total_elements + 1) / 2) or 
            (is_circle and total_elements > 2 and max_count > total_elements / 2)):
            print(f"No valid arrangements possible for this input. Max count ({max_count}) exceeds limit.")
            if progress_callback:
                progress_callback(100, 0)
            return 0, []
        
        async for chunk in async_generate_permutations(
            elements, is_circle, chunk_size=1000, 
            progress_callback=progress_callback, 
            result_file=result_file):
            
            results.extend(chunk)
            total_count = len(results)
            
        # Calculate total count for file output
        if result_file:
            # For circular permutations, we need to adjust
            if is_circle and len(counts) > 1:
                # Calculate the number of equivalent circular arrangements
                for k, v in counter.items():
                    if v == 1:  # If any element appears exactly once
                        total_count = calculate_total_permutations(elements) // total_elements
                        break
                else:
                    # No element appears exactly once, check more complex cases
                    total_count = count_valid_permutations(elements, is_circle)
            else:
                total_count = count_valid_permutations(elements, is_circle)
        
        print(f"Partition calculation complete. Found {total_count:,} valid arrangements.")
        return total_count, results
        
    except Exception as e:
        print(f"Error in async partition calculation: {e}")
        import traceback
        traceback.print_exc()
        return 0, []

def count_valid_permutations(elements, is_circle=False):
    """Count valid permutations by actually validating a sample of permutations."""
    # This function helps estimate the correct count when the theoretical
    # calculation is complex.
    
    # With larger sets, we need a more efficient approach than counting all permutations
    total_perms = calculate_total_permutations(elements)
    
    # For small enough permutation sets, we can count directly
    if total_perms <= 1000000:  # 1 million permutations is reasonable to check
        if is_circle:
            return sum(1 for p in permutations(elements) if is_valid_circular(p))
        else:
            return sum(1 for p in permutations(elements) if is_valid(p))
    
    # For larger sets, we need to use a statistical approach or theoretical calculation
    counter = Counter(elements)
    
    # For circular permutations with elements appearing only once
    if is_circle:
        # Total valid arrangements for a circle can be calculated as (n-1)!/Π(repetitions!)
        # Where n is total elements and repetitions are the counts of each type
        #
        # For cases where each element type appears more than once, we calculate
        # the theoretical maximum and validate a sample
        sample_size = min(100000, total_perms // 100)
        
        # Special case where we have equal numbers of two types (like 3A,3B)
        if len(counter) == 2 and len(set(counter.values())) == 1:
            # For this case, we can use mathematical formula
            n = len(elements)
            k = counter[elements[0]]  # Count of first type
            # The formula is C(n,k) - C(n,k+1) for non-circular
            if k == n // 2:
                from math import comb
                return comb(n, k) - comb(n, k+1)
        
        # Generic sampling approach for other cases
        sample_count = 0
        sample_valid = 0
        
        for p in permutations(elements):
            sample_count += 1
            if is_valid_circular(p):
                sample_valid += 1
            
            if sample_count >= sample_size:
                break
        
        # Estimate full count based on sample ratio
        if sample_count > 0:
            return int(total_perms * (sample_valid / sample_count))
        return 0
    
    # For row permutations (non-circular)
    else:
        # For a row, no two identical elements can be adjacent
        # This is a well-studied problem with some special cases
        
        # Case 1: Two types of elements (A,B)
        if len(counter) == 2:
            counts = list(counter.values())
            # If counts are similar (difference <= 1), then solution exists
            if abs(counts[0] - counts[1]) <= 1:
                # The count is 2 (for which type goes first)
                return 2
            # If one type has more than the other+1, no solution
            else:
                return 0
        
        # For general case, we sample if needed
        sample_size = min(100000, total_perms // 100)
        sample_count = 0
        sample_valid = 0
        
        for p in permutations(elements):
            sample_count += 1
            if is_valid(p):
                sample_valid += 1
            
            if sample_count >= sample_size:
                break
        
        # Estimate full count based on sample ratio
        if sample_count > 0:
            return int(total_perms * (sample_valid / sample_count))
        return 0
