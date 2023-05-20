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
    string = 'سلام'

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
        encoded_l, codes_l = huffman_code_tree(l, binString + '0')
        encoded_string += encoded_l
        d.update(codes_l)
        encoded_r, codes_r = huffman_code_tree(r, binString + '1')
        encoded_string += encoded_r
        d.update(codes_r)
        return encoded_string, d

    freq = {}
    for c in string:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1

    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    nodes = freq

    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))

        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

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
