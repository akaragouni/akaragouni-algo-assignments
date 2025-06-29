import random
import argparse
import sys

class CVMEstimator:
    def __init__(self, size, seed=None):
        self.max_size = size
        if seed is not None:
            random.seed(seed)
        
        self.buffer = {}
        self.p = 1.0
    
    def process_element(self, element):
        """
        Process an element according to Knuth's Algorithm D
        """
        # D4: Remove element from B if it exists
        if element in self.buffer:
            del self.buffer[element]
        
        u = random.random()
        
        if u >= self.p:
            # Skip this element (go back to D2)
            return
        
        if len(self.buffer) < self.max_size:
            # Buffer not full, just insert (element, u) and go back to D2
            self.buffer[element] = u
            return
        
        # D6: Maybe swap element into B
        if not self.buffer:
            self.buffer[element] = u
            return
            
        max_element = max(self.buffer.items(), key=lambda x: x[1])
        max_key, max_volatility = max_element
        
        if u > max_volatility:
            # New element has higher volatility than max in buffer
            # Set p ← u (but don't add element to buffer)
            self.p = u
        else:
            # Replace (max_key, max_volatility) in B by (element, u)
            # and set p ← max_volatility
            del self.buffer[max_key]
            self.buffer[element] = u
            self.p = max_volatility
    
    def estimate_distinct_count(self):
        """
        Return the CVM estimate: |B| / p
        """
        buffer_size = len(self.buffer)
        if buffer_size == 0:
            return 0.0
        
        return buffer_size / self.p

def main():
    parser = argparse.ArgumentParser(description='CVM algorithm for distinct element estimation')
    parser.add_argument('-s', '--seed', type=int, help='Random seed')
    parser.add_argument('size', type=int, help='Buffer size')
    parser.add_argument('filename', help='Input file')
    
    args = parser.parse_args()
    
    try:
        estimator = CVMEstimator(args.size, args.seed)
        
        with open(args.filename, 'r') as f:
            for line in f:
                element = line.strip()
                if element:
                    estimator.process_element(element)
        
        result = estimator.estimate_distinct_count()
        print(int(round(result)))
        
    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 