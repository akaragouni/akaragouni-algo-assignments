import random
import argparse
import sys

class CVMEstimator:
    def __init__(self, buffer_size, seed=None):
        if buffer_size <= 0:
            raise ValueError("Buffer size must be positive")
        
        self.max_size = buffer_size
        self.buffer = {}
        self.p = 1.0
        
        if seed is not None:
            random.seed(seed)
    
    def process_element(self, element):
        """
        Process one element according to Algorithm D steps
        
        D4: Remove element from B if it exists
        D5: Maybe put element in B
        D6: Maybe swap element into B
        """
        u = random.random()
        
        if element in self.buffer:
            del self.buffer[element]
        
        if u >= self.p:
            return
        
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
        """
        Return the CVM estimate: |B| / p
        """
        buffer_size = len(self.buffer)
        if buffer_size == 0:
            return 0.0
        
        return buffer_size / self.p

def process_file(filename, estimator):
    """Process a file line by line"""
    try:
        with open(filename, 'r') as f:
            for line_num, line in enumerate(f, 1):
                element = line.strip()
                if element:
                    estimator.process_element(element)
                elif line_num <= 10:
                    print(f"Warning: Empty line {line_num}", file=sys.stderr)
        return True
    except IOError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(
        description='CVM algorithm for distinct element estimation',
        epilog='Example: python cvm8.py -s 42 100 input.txt'
    )
    parser.add_argument('-s', '--seed', type=int, help='Random seed for reproducible results')
    parser.add_argument('size', type=int, help='Buffer size (must be positive)')
    parser.add_argument('filename', help='Input file containing elements (one per line)')
    
    args = parser.parse_args()
    
    try:
        if args.size <= 0:
            print("Error: Buffer size must be positive", file=sys.stderr)
            sys.exit(1)
        
        estimator = CVMEstimator(args.size, args.seed)
        
        if not process_file(args.filename, estimator):
            sys.exit(1)
        
        result = estimator.estimate_distinct_count()
        print(int(round(result)))
        
    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 