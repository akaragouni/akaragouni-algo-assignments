import sys
import argparse

def generate_graph(s, t):
    n = s + t
    nodes = []
    for i in range(2**n):
        binary = bin(i)[2:].zfill(n)
        if binary.count('0') == s:
            nodes.append(int(binary, 2))
    nodes = sorted(nodes, reverse=True)

    adj = {}
    for node in nodes:
        binary_str = bin(node)[2:].zfill(n)
        adj_nodes = []
        for i in range(n-1):
            if binary_str[i] != binary_str[i+1]:  # Adjacent bits are different
                new_bits = list(binary_str)
                new_bits[i], new_bits[i+1] = new_bits[i+1], new_bits[i]  # Swap
                new_str = ''.join(new_bits)
                new_node = int(new_str, 2)
                adj_nodes.append(new_node)
        adj[node] = sorted(adj_nodes, reverse=True)
    return adj, nodes

def main():
    parser = argparse.ArgumentParser(description='Transposition Graph Generator')
    parser.add_argument('s', type=int, help='Number of 0s')
    parser.add_argument('t', type=int, help='Number of 1s')
    parser.add_argument('method', choices=['graph'], help='Method to display graph')

    args = parser.parse_args()

    if args.method == 'graph':
        adj, nodes = generate_graph(args.s, args.t)
        for node in nodes:
            binary = bin(node)[2:].zfill(args.s + args.t)
            print(f"{node} ({binary}) -> {adj[node]}")

if __name__ == "__main__":
    main()
