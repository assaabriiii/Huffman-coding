import heapq
from collections import defaultdict
import time
import colorama
from colorama import Fore, Style
from art import *

colorama.init(autoreset=True)


def print_with_color(text, color):
    print(f"{color}{text}")


def print_header():
    print(randart())

    header = text2art("Huffman")
    print(header)


def print_huffman_tree(huffman_tree):
    def print_tree(node, level=0):
        indent = '  ' * level
        if isinstance(node, str):
            print_with_color(f"{indent}└─ {node}", Fore.GREEN)
        else:
            print_with_color(f"{indent}├─", Fore.YELLOW)
            print_tree(node.left, level + 1)
            print_tree(node.right, level + 1)

    print_with_color("Huffman Tree:", Fore.YELLOW)
    print_tree(huffman_tree)


def animate_encoding(encoded_string):
    print_with_color("Encoding in progress:", Fore.CYAN)
    for i, bit in enumerate(encoded_string):
        time.sleep(0.5)
        if bit == '0':
            print_with_color(f"╭─ {bit}", Fore.GREEN)
        else:
            print_with_color(f"╭─ {bit}", Fore.YELLOW)
        if i < len(encoded_string) - 1:
            print_with_color("│", Fore.CYAN)
        else:
            print()


def animate_decoding(decoded_string):
    print_with_color("Decoding in progress:", Fore.CYAN)
    for i, char in enumerate(decoded_string):
        time.sleep(0.5)
        print_with_color(f"╰─ {char}", Fore.GREEN)
        if i < len(decoded_string) - 1:
            print_with_color("│", Fore.CYAN)
        else:
            print()


def main():
    string = str(input("Enter your input: "))


    class NodeTree(object):
        def __init__(self, left=None, right=None):
            self.left = left
            self.right = right

        def children(self):
            return (self.left, self.right)

        def nodes(self):
            return (self.left, self.right)

        def __str__(self):
            return '%s_%s' % (self.left, self.right)

    def huffman_code_tree(node, binString=''):
        if type(node) is str:
            return binString, {node: binString}
        (l, r) = node.children()
        encoded_string = ''
        d = dict()
        encoded_r, codes_r = huffman_code_tree(r, binString + '1')  # Switched order for left and right subtrees
        encoded_string += encoded_r
        d.update(codes_r)
        encoded_l, codes_l = huffman_code_tree(l, binString + '0')  # Switched order for left and right subtrees
        encoded_string += encoded_l
        d.update(codes_l)
        return encoded_string, d

    freq = {}
    for c in string:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1

    freq = sorted(freq.items(), key=lambda x: x[1])

    nodes = freq

    while len(nodes) > 1:
        (key1, c1) = nodes[0]
        (key2, c2) = nodes[1]
        nodes = nodes[2:]
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))

        nodes = sorted(nodes, key=lambda x: x[1])

    encoded_string, huffmanCode = huffman_code_tree(nodes[0][0])

    decoded_string = ''
    current_node = nodes[0][0]
    for bit in encoded_string:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right
        if isinstance(current_node, str):
            decoded_string += current_node
            current_node = nodes[0][0]

    print_header()
    print_with_color("Original string:", Fore.YELLOW)
    print_with_color(string, Fore.WHITE)

    print_huffman_tree(nodes[0][0])

    animate_encoding(encoded_string)

    print_with_color("Encoded string:", Fore.YELLOW)
    print_with_color(encoded_string, Fore.WHITE)

    animate_decoding(decoded_string)

    print_with_color("Decoded string:", Fore.YELLOW)
    print_with_color(decoded_string, Fore.WHITE)


if __name__ == '__main__':
    main()


# Huffman code implementation starts here

# to map each character to its Huffman value
codes = {}

# To store the frequency of each character in the input data
freq = defaultdict(int)

# A Huffman tree node
class MinHeapNode:
    def __init__(self, data, freq):
        self.left = None
        self.right = None
        self.data = data
        self.freq = freq

    def __lt__(self, other):
        return self.freq < other.freq

# utility function to print characters along with their Huffman value
def printCodes(root, string):
    if root is None:
        return
    if root.data != '$':
        print(root.data, ":", string)
    printCodes(root.left, string + "0")
    printCodes(root.right, string + "1")

# utility function to store characters along with their Huffman value in a hash table
def storeCodes(root, string):
    if root is None:
        return
    if root.data != '$':
        codes[root.data] = string
    storeCodes(root.left, string + "0")
    storeCodes(root.right, string + "1")

# function to build the Huffman tree and store it in minHeap
def HuffmanCodes(size):
    minHeap = []
    for key in freq:
        minHeap.append(MinHeapNode(key, freq[key]))
    heapq.heapify(minHeap)
    while len(minHeap) != 1:
        left = heapq.heappop(minHeap)
        right = heapq.heappop(minHeap)
        top = MinHeapNode('$', left.freq + right.freq)
        top.left = left
        top.right = right
        heapq.heappush(minHeap, top)
    storeCodes(minHeap[0], "")

# utility function to store the frequency of each character in the input string
def calcFreq(string, n):
    for i in range(n):
        freq[string[i]] += 1

# function to iterate through the encoded string s
# if s[i]=='1', then move to node->right
# if s[i]=='0', then move to node->left
# if leaf node, append the node->data to our output string
def decode_file(root, s):
    ans = ""
    curr = root
    n = len(s)
    for i in range(n):
        if s[i] == '0':
            curr = curr.left
        else:
            curr = curr.right

        # reached leaf node
        if curr.left is None and curr.right is None:
            ans += curr.data
            curr = root
    return ans + '\0'


# Driver code
if __name__ == "__main__":
    string = str(input("Enter your input: "))
    calcFreq(string, len(string))
