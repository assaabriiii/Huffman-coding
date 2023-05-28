import heapq
from collections import defaultdict
import tkinter as tk
import colorama
from colorama import Fore, Style
from art import *

colorama.init()

window = tk.Tk()
window.title("Huffman Tree")

canvas = tk.Canvas(window, width=800, height=600)
canvas.pack()


def draw_tree(node, x, y, dx):
    if node is None:
        return

    canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="white")
    canvas.create_text(x, y, text=f"{node.data}\n{node.freq}", font="Arial 12 bold")

    if node.left is not None:
        x_left = x - dx
        y_left = y + 80
        canvas.create_line(x, y + 20, x_left, y_left - 20, width=2)
        draw_tree(node.left, x_left, y_left, dx // 2)

    if node.right is not None:
        x_right = x + dx
        y_right = y + 80
        canvas.create_line(x, y + 20, x_right, y_right - 20, width=2)
        draw_tree(node.right, x_right, y_right, dx // 2)


codes = {}
freq = defaultdict(int)


class MinHeapNode:
    def __init__(self, data, freq):
        self.left = None
        self.right = None
        self.data = data
        self.freq = freq

    def __lt__(self, other):
        return self.freq < other.freq


def printCodes(root, code_str):
    if root is None:
        return
    if root.data != '$':
        print(f"{Fore.GREEN}{root.data}{Style.RESET_ALL}: {code_str}")
    printCodes(root.left, code_str + "0")
    printCodes(root.right, code_str + "1")


def storeCodes(root, code_str):
    if root is None:
        return
    if root.data != '$':
        codes[root.data] = code_str
    storeCodes(root.left, code_str + "0")
    storeCodes(root.right, code_str + "1")


def HuffmanCodes(size):
    global minHeap
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


def calcFreq(input_str, n):
    for i in range(n):
        freq[input_str[i]] += 1


def decode_file(root, s):
    ans = ""
    curr = root
    n = len(s)
    for i in range(n):
        if s[i] == '0':
            curr = curr.left
        else:
            curr = curr.right

        if curr.left is None and curr.right is None:
            ans += curr.data
            curr = root
    return ans + '\0'


def compare_with_ascii(input_str):
    ascii_code = ""
    for char in input_str:
        ascii_code += str(ord(char)) + " "
    print(f"\n{Fore.YELLOW}ASCII Code of the String:{Style.RESET_ALL}")
    print(ascii_code)

    huffman_code = ""
    for char in input_str:
        huffman_code += codes[char] + " "
    print(f"\n{Fore.YELLOW}Huffman Code of the String:{Style.RESET_ALL}")
    print(huffman_code)

    if ascii_code == huffman_code:
        print(f"\n{Fore.GREEN}Huffman Code matches ASCII Code.{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}Huffman Code does not match ASCII Code.{Style.RESET_ALL}")


def visualize_frequency_distribution(input_str):
    frequency = defaultdict(int)
    for char in input_str:
        frequency[char] += 1

    print(f"\n{Fore.YELLOW}Frequency Distribution:{Style.RESET_ALL}")
    for key in sorted(frequency):
        print(f"{Fore.GREEN}{key}{Style.RESET_ALL}: {frequency[key]}")

    # Bar chart visualization
    import matplotlib.pyplot as plt

    plt.bar(frequency.keys(), frequency.values())
    plt.xlabel("Characters")
    plt.ylabel("Frequency")
    plt.title("Frequency Distribution")
    plt.show()


def efficiency_comparison(input_str):
    import sys
    import zlib
    from collections import Counter

    encoded_string = ""
    calcFreq(input_str, len(input_str))
    HuffmanCodes(len(input_str))
    for char in input_str:
        encoded_string += codes[char]

    def rle_encode(input_str):
        encoded = ""
        count = 1
        for i in range(1, len(input_str)):
            if input_str[i] == input_str[i - 1]:
                count += 1
            else:
                encoded += input_str[i - 1] + str(count)
                count = 1
        encoded += input_str[-1] + str(count)
        return encoded

    rle_encoded_string = rle_encode(input_str)

    def lzw_compress(input_str):
        dictionary = {chr(i): i for i in range(256)}
        next_code = 256
        compressed = []
        w = ""
        for c in input_str:
            wc = w + c
            if wc in dictionary:
                w = wc
            else:
                compressed.append(dictionary[w])
                dictionary[wc] = next_code
                next_code += 1
                w = c
        if w:
            compressed.append(dictionary[w])
        return compressed

    lzw_compressed = lzw_compress(input_str)

    # Compression Ratios
    input_size = sys.getsizeof(input_str)
    huffman_size = sys.getsizeof(int(encoded_string, 2)) // 8
    rle_size = sys.getsizeof(rle_encoded_string) // 8
    lzw_size = sys.getsizeof(bytes(lzw_compressed)) // 8
    zlib_size = sys.getsizeof(zlib.compress(input_str.encode())) // 8

    print(f"\n{Fore.YELLOW}Compression Efficiency Comparison:{Style.RESET_ALL}")
    print(f"Input Size: {input_size} bytes")
    print(f"Huffman Encoded Size: {huffman_size} bytes")
    print(f"RLE Encoded Size: {rle_size} bytes")
    print(f"LZW Compressed Size: {lzw_size} bytes")
    print(f"Zlib Compressed Size: {zlib_size} bytes")


def compress_file(file_path):
    with open(file_path, 'r') as file:
        input_str = file.read().replace('\n', '')

    encoded_string = ""
    calcFreq(input_str, len(input_str))
    HuffmanCodes(len(input_str))
    for char in input_str:
        encoded_string += codes[char]

    compressed_file_path = file_path + '.compressed'
    with open(compressed_file_path, 'w') as file:
        file.write(encoded_string)

    print(f"\n{Fore.GREEN}File compressed successfully. Compressed file: {compressed_file_path}{Style.RESET_ALL}")


def calculate_compression_ratio(input_str, encoded_str):
    input_size = len(input_str) * 8  
    encoded_size = len(encoded_str)  
    compression_ratio = (input_size - encoded_size) / input_size
    return compression_ratio

if __name__ == "__main__":
    tprint("Huffman", font="random")
    minHeap = []
    input_str = "Hello world"
    encodedString, decodedString = "", ""
    calcFreq(input_str, len(input_str))
    HuffmanCodes(len(input_str))
    print(f"{Fore.CYAN}Character With their Frequencies:{Style.RESET_ALL}")
    for key in sorted(codes):
        print(f"{Fore.GREEN}{key}{Style.RESET_ALL}: {codes[key]}")

    for i in input_str:
        encodedString += codes[i]

    print(f"\n{Fore.YELLOW}Encoded Huffman data:{Style.RESET_ALL}")
    print(encodedString)

    decodedString = decode_file(minHeap[0], encodedString)
    print(f"\n{Fore.YELLOW}Decoded Huffman Data:{Style.RESET_ALL}")
    print(decodedString)
    
    compression_ratio = calculate_compression_ratio(input_str, encodedString)
    print(f"\n{Fore.YELLOW}Compression Ratio:{Style.RESET_ALL}")
    print(f"{compression_ratio * 100:.2f}%")

    dx = 200
    draw_tree(minHeap[0], 400, 50, dx)

    compare_with_ascii(input_str)
    visualize_frequency_distribution(input_str)
    efficiency_comparison(input_str)
    
    compress_file("file.txt")

    window.mainloop()