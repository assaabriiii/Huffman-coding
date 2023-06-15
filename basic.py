from collections import defaultdict
import tkinter as tk
import colorama
from colorama import Fore, Style
from art import *

colorama.init()



# Function to draw the Huffman tree on a tkinter canvas
def draw_tree(node, x, y, dx):
    if node is None:
        return
    
    # Draw a circle for the current node
    canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="white")
    canvas.create_text(x, y, text=f"{node.data}\n{node.freq}", font="Arial 12 bold")
    
    # Recursively draw the left and right subtrees
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




# Class representing a node in the Huffman tree
class MinHeapNode:
    def __init__(self, data, freq):
        self.left = None
        self.right = None
        self.data = data
        self.freq = freq

    def __lt__(self, other):
        return self.freq < other.freq
    
# Function to print the Huffman codes for each character
def printCodes(root, code_str):
    if root is None:
        return
    if root.data != '$':
        print(f"{Fore.GREEN}{root.data}{Style.RESET_ALL}: {code_str}")
    printCodes(root.left, code_str + "0")
    printCodes(root.right, code_str + "1")


# Function to store the Huffman codes for each character
def storeCodes(root, code_str):
    if root is None:
        return
    if root.data != '$':
        codes[root.data] = code_str
    storeCodes(root.left, code_str + "0")
    storeCodes(root.right, code_str + "1")

# Heap operations
def _siftdown(heap, startpos, pos):
    newitem = heap[pos]
    while pos > startpos:
        parentpos = (pos - 1) >> 1
        parent = heap[parentpos]
        if newitem < parent:
            heap[pos] = parent
            pos = parentpos
            continue
        break
    heap[pos] = newitem

# Heap operations
def _siftup(heap, pos):
    endpos = len(heap)
    startpos = pos
    newitem = heap[pos]
    childpos = 2*pos + 1    
    while childpos < endpos:
        rightpos = childpos + 1
        if rightpos < endpos and not heap[childpos] < heap[rightpos]:
            childpos = rightpos
        heap[pos] = heap[childpos]
        pos = childpos
        childpos = 2*pos + 1
    heap[pos] = newitem
    _siftdown(heap, startpos, pos)

# Heap operations
def heappop(heap):
    lastelt = heap.pop()    
    if heap:
        returnitem = heap[0]
        heap[0] = lastelt
        _siftup(heap, 0)
        return returnitem
    return lastelt

# Heap operations
def heapify(x):
    n = len(x)
    for i in reversed(range(n//2)):
        _siftup(x, i)

# Heap operations   
def heappush(heap, item):
    """Push item onto heap, maintaining the heap invariant."""
    heap.append(item)
    _siftdown(heap, 0, len(heap)-1)


# Function to calculate the Huffman codes for the input characters
def HuffmanCodes(size):
    global minHeap
    for key in freq:
        minHeap.append(MinHeapNode(key, freq[key]))
    heapify(minHeap)
    while len(minHeap) != 1:
        left = heappop(minHeap)
        right = heappop(minHeap)
        top = MinHeapNode('$', left.freq + right.freq)
        top.left = left
        top.right = right
        heappush(minHeap, top)
    storeCodes(minHeap[0], "")


# Function to calculate the frequency of characters in the input string
def calcFreq(input_str, n):
    for i in range(n):
        freq[input_str[i]] += 1


# Function to decode a Huffman-encoded string using the Huffman tree
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


# Function to compare the Huffman codes with ASCII codes
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


# Function to visualize the frequency distribution of characters in the input string
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


# Function to compare the efficiency of different compression methods
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


# Function to compress a file using Huffman coding
def compress_file(file_path):
    
    # Huffman coding and compression
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


# Function to calculate the compression ratio for a Huffman-encoded string
def calculate_compression_ratio(input_str, encoded_str):
    input_size = len(input_str) * 8  
    encoded_size = len(encoded_str)  
    compression_ratio = (input_size - encoded_size) / input_size
    return compression_ratio

# Main program loop
flag = 1 
while flag == 1:
    # Initialize variables
    codes = {}
    freq = defaultdict(int) 
    window = tk.Tk()
    window.title("Huffman Tree")

    canvas = tk.Canvas(window, width=800, height=600)
    canvas.pack()
    tprint("Huffman", font="random")
    input_str = input("Enter your string (print 'exit' to quit): ")
    
    if input_str.lower() == "exit": 
        exit()
        
    minHeap = []
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
    minHeap = []
    print(minHeap)



while flag == 0 : 
    
    
    persian_words = [
    "سلام",
    "خداحافظ",
    "ممنون",
    "بله",
    "نه",
    "ببخشید",
    "متشکرم",
    "بفرمایید",
    "لطفاً",
    "کجا",
    "چطور",
    "کی",
    "چرا",
    "چه",
    "اینجا",
    "آنجا",
    "الان",
    "فقط",
    "همین",
    "همه",
    "کار",
    "زندگی",
    "عشق",
    "دوست",
    "خوشحال",
    "ناراحت",
    "ترس",
    "آب",
    "آتش",
    "هوا",
    "خوراک",
    "شراب",
    "خواب",
    "عکس",
    "کتاب",
    "مدرسه",
    "دانشگاه",
    "کامپیوتر",
    "تلویزیون",
    "موبایل",
    "ماشین",
    "خانه",
    "خیابان",
    "شهر",
    "روستا",
    "دریا",
    "کوه",
    "جنگل",
    "گل",
    "درخت",
    "ماه",
    "خورشید",
    "ستاره",
    "پدر",
    "مادر",
    "برادر",
    "خواهر",
    "پسر",
    "دختر",
    "دوست",
    "عمو",
    "خاله",
    "دایی",
    "همسر",
    "بچه",
    "نوه",
    "پدربزرگ",
    "مادربزرگ",
    "خوانواده",
    "سفر",
    "تعطیلات",
    "کارت",
    "پول",
    "موزیک",
    "فیلم",
    "ورزش",
    "بازی",
    "هنر",
    "آشپزی",
    "عید",
    "تولد",
    "عروسی",
    "جشن",
    "هدیه",
    "مهمان",
    "سفارش",
    "قرض",
    "دفتر",
    "قرار",
    "نامه",
    "پیام",
    "سوال",
    "جواب",
    "نظر",
    "احساس",
    "رویا",
    "امیر",
    "حسین",
    "حسن",
    "رضا",
    "انار"
    ]

    avg = 0
    counter = 0 
    
    for input_str in persian_words:
        counter += 1  
        codes = {}
        
        freq = defaultdict(int) 
        minHeap = []
        encodedString, decodedString = "", ""
        calcFreq(input_str, len(input_str))
        HuffmanCodes(len(input_str))
        
        for key in sorted(codes):
            print(f"{key}: {codes[key]}")
        
        for i in input_str:
            encodedString += codes[i]
            
        
        
        decodedString = decode_file(minHeap[0], encodedString)
        
        compression_ratio = calculate_compression_ratio(input_str, encodedString)
        cr = int(compression_ratio * 100)
        avg += cr 

        file = open("result.txt", "a")
        content = str(encodedString) + " : " + str(decodedString) + " ratio " + " : " + str(cr) + "\n"
        file.write(content)
        print(counter)
        from time import sleep 
        sleep(0.2)
        print(input_str)
        if counter == 100: 
            break

    avg = avg / 100 
    content = "total final average comperssion ratio:" + str(avg) + "\n"
    file.write(content)
    break


