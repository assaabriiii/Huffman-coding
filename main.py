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

print("Original string:", string)
print("Encoded string:", encoded_string)
print("Decoded string:", decoded_string)