class Node: 
    def __init__(self, char, frequancy): 
        self.char = char 
        self.frequancy = frequancy 
        self.left = None 
        self.right = None 

def calculate_frequency(text): 
    frequency = {}
    for char in text: 
        if char in frequency: 
            frequency[char] += 1 
        else: 
            frequency[char] = 1 
    return frequency


def create_prority_queue(frequancy):
    priority_queue = []
    
    for char, freq in frequancy.items():
        node = Node(char, freq)
        priority_queue.append(node)
        
        
    priority_queue.sort(key=lambda x: x.frequancy)
    return priority_queue


def build_huffman_tree(priority_queue):
    while len(priority_queue) > 1: 
        node1 = priority_queue.pop(0)
        node2 = priority_queue.pop(0)
        
        combined = node1.frequancy + node2.frequancy
        combined_node = Node(None, combined)
        
        combined_node.left = node1 
        combined_node.right = node2 
        
        priority_queue.append(combined_node)
        
        priority_queue.sort(key=lambda x: x.frequancy)
        
    return priority_queue[0] if priority_queue else None


def assign_codes(node, code, codes): 
    if node.char: 
        codes[node.char] = code 
    else: 
        assign_codes(node.left, code + '0', codes)
        assign_codes(node.right, code + '1', codes)


def build_huffman_tree_and_get_codes(text): 
    frequancy = calculate_frequency(text=text)
    priority_queue = create_prority_queue(frequancy=frequancy)
    huffman_tree = build_huffman_tree(priority_queue=priority_queue)
    codes = {}
    assign_codes(huffman_tree, '', codes)
    return huffman_tree, codes


text = "Hello world"

huffman_tree, codes = build_huffman_tree_and_get_codes(text)

print(codes)