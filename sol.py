from itertools import product

def is_valid_combination(counts):
    """
    Kiểm tra tính hợp lệ của tổ hợp counts.
    """
    counts_as_text = (
        f"Trong câu này số chữ số 0 là {counts[0]}, "
        f"số chữ số 1 là {counts[1]}, "
        f"số chữ số 2 là {counts[2]}, "
        f"số chữ số 3 là {counts[3]}, "
        f"số chữ số 4 là {counts[4]}, "
        f"số chữ số 5 là {counts[5]}, "
        f"số chữ số 6 là {counts[6]}, "
        f"số chữ số 7 là {counts[7]}, "
        f"số chữ số 8 là {counts[8]}, "
        f"số chữ số 9 là {counts[9]}."
    )
    actual_counts = [counts_as_text.count(str(i)) for i in range(10)]
    return counts == actual_counts

def find_valid_combinations():
    """
    Tìm tổ hợp hợp lệ.
    """
    fixed_counts = [1, 0, 0, 0, 0, 0, 0, 0, 1, 1]
    valid_combinations = []

    for combination in product(range(10), repeat=7):
        counts = fixed_counts[:]
        counts[1:8] = combination

        if is_valid_combination(counts):
            valid_combinations.append(tuple(counts))

    return valid_combinations

if __name__ == "__main__":
    combinations = find_valid_combinations()
    print(f"Số tổ hợp hợp lệ: {len(combinations)}")
    for combo in combinations:
        print(combo)
