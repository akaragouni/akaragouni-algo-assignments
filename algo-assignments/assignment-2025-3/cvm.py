import random

def count_distinct_sampled(elements, sample_probability=0.5):
    """Count distinct elements using random sampling"""
    sampled_set = set()
    
    for element in elements:
        # Flip a coin for each element
        if random.random() < sample_probability:
            sampled_set.add(element)
    
    # Scale up the result
    estimated_count = len(sampled_set) / sample_probability
    return estimated_count

def main():
    # Test with a simple sequence
    test_sequence = [1, 2, 3, 2, 4, 1, 5, 3, 6]
    
    print("Running multiple trials to see the variation:")
    for trial in range(5):
        random.seed(trial)  # For reproducible results
        result = count_distinct_sampled(test_sequence, 0.5)
        print(f"Trial {trial + 1}: Estimated count = {result:.1f}")
    
    exact = len(set(test_sequence))
    print(f"\nExact count: {exact}")

if __name__ == "__main__":
    main() 