import heapq
from bitarray import bitarray
from graphviz import Digraph

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_table(text):
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    return freq

def build_huffman_tree(freq_table):
    heap = [Node(char, freq) for char, freq in freq_table.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

def generate_huffman_codes(root, current_code="", huffman_codes={}):
    if root is None:
        return
    
    if root.char is not None:
        huffman_codes[root.char] = current_code

    generate_huffman_codes(root.left, current_code + "0", huffman_codes)
    generate_huffman_codes(root.right, current_code + "1", huffman_codes)

    return huffman_codes

def huffman_compress(text):
    freq_table = build_frequency_table(text)
    huffman_tree = build_huffman_tree(freq_table)
    huffman_codes = generate_huffman_codes(huffman_tree)

    # Use a bitarray to accumulate the binary data
    encoded_bits = bitarray()

    for char in text:
        encoded_bits.extend(huffman_codes[char])  # Add the Huffman code bits to the bitarray

    padding = 8 - len(encoded_bits) % 8
    encoded_bits.extend([0] * padding)
    # Add padding if necessary

    # Convert the bitarray to bytes
    byte_array = encoded_bits.tobytes()

    return huffman_codes, byte_array, padding

def huffman_decompress(compressed_data, huffman_codes, padding):
    reverse_codes = {v: k for k, v in huffman_codes.items()}
    
    # Convert the byte data to a bitarray
    binary_string = bitarray()
    binary_string.frombytes(compressed_data)
    
    # Remove the padding bits
    binary_string = binary_string[:-padding]

    decoded_text = ""
    temp_code = ""
    for bit in binary_string:
        temp_code += str(bit)
        if temp_code in reverse_codes:
            decoded_text += reverse_codes[temp_code]
            temp_code = ""

    return decoded_text

# Function to visualize the Huffman Tree using Graphviz
def visualize_huffman_tree(root, dot=None, parent=None, direction=None):
    if dot is None:
        dot = Digraph()

    if root is not None:
        # Create a node for the current character
        if root.char is not None:
            dot.node(str(root), f"{root.char} ({root.freq})")
        else:
            dot.node(str(root), f"({root.freq})")

        # Add edges between the parent node and the children
        if parent is not None:
            dot.edge(str(parent), str(root), label=direction)

        # Recursively visualize the left and right children
        if root.left:
            visualize_huffman_tree(root.left, dot, root, '0')
        if root.right:
            visualize_huffman_tree(root.right, dot, root, '1')

    return dot

# Function to create and show the Huffman Tree visualization in a PNG
def save_huffman_tree_image(huffman_tree, filename='huffman_tree'):
    dot = visualize_huffman_tree(huffman_tree)
    dot.render(filename, format='png')
