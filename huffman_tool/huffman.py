import heapq
import os
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

    encoded_text = "".join(huffman_codes[char] for char in text)
    padding = 8 - len(encoded_text) % 8
    encoded_text += "0" * padding

    byte_array = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte_array.append(int(encoded_text[i:i+8], 2))

    return huffman_codes, bytes(byte_array), padding

def huffman_decompress(compressed_data, huffman_codes, padding):
    reverse_codes = {v: k for k, v in huffman_codes.items()}
    binary_string = "".join(f"{byte:08b}" for byte in compressed_data)
    binary_string = binary_string[:-padding]
    # Remove padding

    decoded_text = ""
    temp_code = ""
    for bit in binary_string:
        temp_code += bit
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
