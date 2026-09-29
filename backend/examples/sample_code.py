def find_max(numbers: list) -> int:
    if not numbers:
        raise ValueError("List cannot be empty")
    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val