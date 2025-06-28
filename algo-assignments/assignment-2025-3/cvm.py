import random

def count_distinct_with_threshold(elements, buffer_size=5):
    """Count distinct elements using volatility and probability threshold"""
    buffer = {}  # element -> volatility
    p = 1.0      # Probability threshold (starts at maximum)
    
    for element in elements:
        volatility = random.random()
        
        print(f"Processing {element} with volatility {volatility:.3f}, p = {p:.3f}")
        
        # Remove element if it exists
        if element in buffer:
            print(f"  Removing existing {element}")
            del buffer[element]
        
        # Only consider elements with volatility < p
        if volatility >= p:
            print(f"  Skipping {element} (volatility >= p)")
            continue
        
        # Add to buffer if there's space
        if len(buffer) < buffer_size:
            buffer[element] = volatility
            print(f"  Added {element} to buffer")
        else:
            # Buffer is full - need to make room or adjust p
            max_element = max(buffer.items(), key=lambda x: x[1])
            max_key, max_volatility = max_element
            
            print(f"  Buffer full! Max volatility element: {max_key} ({max_volatility:.3f})")
            
            if volatility > max_volatility:
                # New element has higher volatility - adjust p but don't add
                p = volatility
                print(f"  New p = {p:.3f}")
            else:
                # Replace highest volatility element
                del buffer[max_key]
                buffer[element] = volatility
                p = max_volatility
                print(f"  Replaced {max_key} with {element}, new p = {p:.3f}")
    
    # Estimate: buffer_size / p
    estimate = len(buffer) / p
    print(f"\nFinal buffer: {buffer}")
    print(f"Final p: {p:.3f}")
    
    return estimate

def main():
    test_sequence = [1, 2, 3, 4, 5, 6, 7, 8]
    
    print("Testing with probability threshold:")
    random.seed(42)
    result = count_distinct_with_threshold(test_sequence, buffer_size=3)
    print(f"\nEstimated count: {result:.2f}")
    
    exact = len(set(test_sequence))
    print(f"Exact count: {exact}")

if __name__ == "__main__":
    main() 