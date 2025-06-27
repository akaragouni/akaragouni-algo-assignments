def count_distinct_exact(elements):
    """Count distinct elements exactly using a set"""
    distinct_set = set()
    
    for element in elements:
        distinct_set.add(element)
    
    return len(distinct_set)

def main():
    # Test with a simple sequence
    test_sequence = [1, 2, 3, 2, 4, 1, 5, 3, 6]
    
    result = count_distinct_exact(test_sequence)
    print(f"Exact distinct count: {result}")
    print(f"Elements: {sorted(set(test_sequence))}")

if __name__ == "__main__":
    main() 