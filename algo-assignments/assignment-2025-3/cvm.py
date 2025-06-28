import random

class CVMEstimator:
    def __init__(self, buffer_size):
        self.max_size = buffer_size
        self.buffer = {}
        self.p = 1.0
    
    def process_element(self, element):
        """Process one element according to Algorithm D steps"""

        u = random.random()

        if element in self.buffer:
            del self.buffer[element]
        
        if u >= self.p:
            return
        
        if len(self.buffer) < self.max_size:
            self.buffer[element] = u
            return
        
        # Find element with maximum volatility
        if not self.buffer:
            self.buffer[element] = u
            return
            
        max_element = max(self.buffer.items(), key=lambda x: x[1])
        max_key, max_volatility = max_element
        
        if u > max_volatility:
            # New element has higher volatility than max in buffer
            self.p = u
        else:
            # Replace max element with new element
            del self.buffer[max_key]
            self.buffer[element] = u
            self.p = max_volatility
    
    def estimate_distinct_count(self):
        """Return the CVM estimate: |B| / p"""
        if len(self.buffer) == 0:
            return 0.0
        return len(self.buffer) / self.p

def main():
    # Test the estimator
    estimator = CVMEstimator(buffer_size=3)
    
    test_sequence = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    print("Processing elements:")
    for element in test_sequence:
        estimator.process_element(element)
        estimate = estimator.estimate_distinct_count()
        print(f"After {element}: buffer={list(estimator.buffer.keys())}, "
              f"p={estimator.p:.3f}, estimate={estimate:.2f}")
    
    final_estimate = estimator.estimate_distinct_count()
    exact_count = len(set(test_sequence))
    
    print(f"\nFinal estimate: {final_estimate:.2f}")
    print(f"Exact count: {exact_count}")
    print(f"Error: {abs(final_estimate - exact_count):.2f}")

if __name__ == "__main__":
    random.seed(42)
    main() 