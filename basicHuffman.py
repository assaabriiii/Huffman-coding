import heapq
from collections import defaultdict
import tkinter as tk
import colorama
from colorama import Fore, Style
from art import * 

# Initialize colorama
colorama.init()



# Create a tkinter window
window = tk.Tk()
window.title("Huffman Tree")

# Create a canvas to draw the Huffman tree
canvas = tk.Canvas(window, width=800, height=600)
canvas.pack()

# Function to draw a node and its children recursively
def draw_tree(node, x, y, dx):
    if node is None:
        return

    # Draw the node
    canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="white")
    canvas.create_text(x, y, text=f"{node.data}\n{node.freq}", font="Arial 12 bold")

    # Draw left child
    if node.left is not None:
        x_left = x - dx
        y_left = y + 80
        canvas.create_line(x, y + 20, x_left, y_left - 20, width=2)
        draw_tree(node.left, x_left, y_left, dx // 2)

    # Draw right child
    if node.right is not None:
        x_right = x + dx
        y_right = y + 80
        canvas.create_line(x, y + 20, x_right, y_right - 20, width=2)
        draw_tree(node.right, x_right, y_right, dx // 2)


codes = {}

# To store the frequency of character of the input data
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

# utility function to print characters along with
# their Huffman value
def printCodes(root, str):
	if root is None:
		return
	if root.data != '$':
		print(f"{Fore.GREEN}{root.data}{Style.RESET_ALL}: {str}")
	printCodes(root.left, str + "0")
	printCodes(root.right, str + "1")

# utility function to store characters along with
# their Huffman value in a hash table
def storeCodes(root, str):
	if root is None:
		return
	if root.data != '$':
		codes[root.data] = str
	storeCodes(root.left, str + "0")
	storeCodes(root.right, str + "1")

# function to build the Huffman tree and store it
# in minHeap
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

# utility function to store map each character with its
# frequency in input string
def calcFreq(str, n):
	for i in range(n):
		freq[str[i]] += 1

# function iterates through the encoded string s
# if s[i]=='1' then move to node->right
# if s[i]=='0' then move to node->left
# if leaf node append the node->data to our output string
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
	tprint("Huffman", font="random")
	minHeap = []
	str = "سلام"
	encodedString, decodedString = "", ""
	calcFreq(str, len(str))
	HuffmanCodes(len(str))
	print(f"{Fore.CYAN}Character With their Frequencies:{Style.RESET_ALL}")
	for key in sorted(codes):
		print(f"{Fore.GREEN}{key}{Style.RESET_ALL}: {codes[key]}")

	for i in str:
		encodedString += codes[i]

	print(f"\n{Fore.YELLOW}Encoded Huffman data:{Style.RESET_ALL}")
	print(encodedString)

	# Function call
	decodedString = decode_file(minHeap[0], encodedString)
	print(f"\n{Fore.YELLOW}Decoded Huffman Data:{Style.RESET_ALL}")
	print(decodedString)

	# Draw the Huffman tree
	dx = 200  # Horizontal distance between nodes
	draw_tree(minHeap[0], 400, 50, dx)

	# Start the tkinter main loop
	window.mainloop()
