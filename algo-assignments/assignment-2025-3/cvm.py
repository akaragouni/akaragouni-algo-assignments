import random
import argparse
import sys

class CVMEstimator:
    def __init__(self, buffer_size, seed=None):
        self.max_size = buffer_size
        self.buffer = {}
        self.p = 1.0
        
        if seed is not None:
            random.seed(seed)
    
    def process_element(self, element):
        """Process one element according to Algorithm D steps"""
        u = random.random()
        
        if element in self.buffer:
            del self.buffer[element]
        
        if u >= self.p:
            return  # Skip this element
        
        if len(self.buffer) < self.max_size:
            self.buffer[element] = u
            return
        
        if not self.buffer:
            self.buffer[element] = u
            return
            
        max_element = max(self.buffer.items(), key=lambda x: x[1])
        max_key, max_volatility = max_element
        
        if u > max_volatility:
            self.p = u
        else:
            del self.buffer[max_key]
            self.buffer[element] = u
            self.p = max_volatility
    
    def estimate_distinct_count(self):
        """Return the CVM estimate: |B| / p"""
        if len(self.buffer) == 0:
            return 0.0
        return len(self.buffer) / self.p

def main():
    parser = argparse.ArgumentParser(description='CVM algorithm for distinct element estimation')
    parser.add_argument('-s', '--seed', type=int, help='Random seed')
    parser.add_argument('size', type=int, help='Buffer size')
    parser.add_argument('filename', help='Input file')
    
    args = parser.parse_args()
    
    try:
        # Initialize estimator
        estimator = CVMEstimator(args.size, args.seed)
        
        with open(args.filename, 'r') as f:
            for line in f:
                element = line.strip()
                if element:  # Skip empty lines
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