import random

def count_distinct_with_volatility(elements, buffer_size=5):
    buffer = {}
    
    for element in elements:
        # Generate a new volatility for this element
        volatility = random.random()
        
        # Remove element if it exists (gets new volatility)
        if element in buffer:
            del buffer[element]
        
        # Add element with its volatility
        if len(buffer) < buffer_size:
            buffer[element] = volatility
            print(f"Added {element} with volatility {volatility:.3f}")
        else:
            print(f"Buffer full! Element {element} with volatility {volatility:.3f} not added")
    
    print(f"\nFinal buffer: {dict(sorted(buffer.items(), key=lambda x: x[1]))}")
    
    return len(buffer)

def main():
    test_sequence = [1, 2, 3, 4, 5, 6, 7, 8]
    
    print("Testing volatility-based sampling:")
    random.seed(42)  # For reproducible results
    result = count_distinct_with_volatility(test_sequence, buffer_size=4)
    print(f"\nBuffer size: {result}")
    
    exact = len(set(test_sequence))
    print(f"Exact count: {exact}")

if __name__ == "__main__":
    main() 