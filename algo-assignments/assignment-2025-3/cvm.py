import random

def count_distinct_fixed_sampling(elements, sample_probability=0.5, buffer_size=10):
    sampled_set = set()
    
    for element in elements:
        # First, remove the element if it exists
        if element in sampled_set:
            sampled_set.remove(element)
        
        # Then decide whether to add it back
        if random.random() < sample_probability:
            if len(sampled_set) < buffer_size:
                sampled_set.add(element)
            else:
                print(f"Buffer full! Cannot add {element}")
    
    # Scale up the result
    estimated_count = len(sampled_set) / sample_probability
    return estimated_count

def main():
    # Test with a sequence that will cause buffer overflow
    test_sequence = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    
    print("Testing with fixed sampling and buffer limit:")
    for trial in range(3):
        random.seed(trial)
        result = count_distinct_fixed_sampling(test_sequence, 0.5, buffer_size=5)
        print(f"Trial {trial + 1}: Estimated count = {result:.1f}")
    
    exact = len(set(test_sequence))
    print(f"\nExact count: {exact}")
    print("Notice: Buffer overflow prevents accurate estimation!")

if __name__ == "__main__":
    main() 