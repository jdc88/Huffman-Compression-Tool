# Huffman Commpression Tool
# Josephine Choi
# Johnson Tran
# Alex Islas

import tkinter as tk
from tkinter import filedialog
import pickle
from huffman import huffman_compress, huffman_decompress
from huffman import build_frequency_table, build_huffman_tree, save_huffman_tree_image

def compress_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return

    with open(file_path, 'r') as file:
        text = file.read()

    # Perform Huffman compression
    huffman_codes, compressed_data, padding = huffman_compress(text)
    huffman_tree = build_huffman_tree(build_frequency_table(text))

    # Save the compressed data to file
    with open("compressed.bin", "wb") as compressed_file:
        compressed_file.write(compressed_data)

    # Save the Huffman codes and padding info
    with open("huffman_codes.pkl", "wb") as code_file:
        pickle.dump((huffman_codes, padding), code_file)

    # Calculate file sizes
    original_size = len(text.encode('utf-8'))  # in bytes
    compressed_size = len(compressed_data)
    compression_ratio = (compressed_size / original_size) * 100 if original_size > 0 else 0  # as a percentage

    # Display Huffman codes in the GUI
    code_display.delete("1.0", tk.END)
    code_display.insert(tk.END, "Huffman Codes:\n")
    for char, code in huffman_codes.items():
        code_display.insert(tk.END, f"'{char}': {code}\n")

    # Visualize the Huffman Tree and save it as PNG
    save_huffman_tree_image(huffman_tree)

    # Update status and size labels
    status_label.config(text="File Compressed Successfully! Output: compressed.bin and huffman_tree.png")
    original_size_label.config(text=f"Original Size: {original_size} bytes")
    compressed_size_label.config(text=f"Compressed Size: {compressed_size} bytes")
    compression_ratio_label.config(text=f"Compression Ratio: {compression_ratio:.2f}%")

def decompress_file():
    try:
        # Read the compressed data
        with open("compressed.bin", "rb") as compressed_file:
            compressed_data = compressed_file.read()

        # Read the Huffman codes and padding
        with open("huffman_codes.pkl", "rb") as code_file:
            huffman_codes, padding = pickle.load(code_file)

        # Decompress the file
        decoded_text = huffman_decompress(compressed_data, huffman_codes, padding)

        # Write the decoded text to a file
        with open("decompressed.txt", "w") as output_file:
            output_file.write(decoded_text)

        decoded_display.delete("1.0", tk.END)
        decoded_display.insert(tk.END, "Decoded Text:\n")
        decoded_display.insert(tk.END, decoded_text)

        status_label.config(text="File Decompressed Successfully!")
    
    except FileNotFoundError:
        status_label.config(text="Error: No compressed file found.")

root = tk.Tk()
root.title("Huffman Compression Tool")

frame = tk.Frame(root)
frame.pack(pady=10)

# Buttons for compressing and decompressing
compress_btn = tk.Button(frame, text="Compress File", command=compress_file)
compress_btn.grid(row=0, column=0, padx=5)

decompress_btn = tk.Button(frame, text="Decompress File", command=decompress_file)
decompress_btn.grid(row=0, column=1, padx=5)

# Text widget to display Huffman codes
code_display = tk.Text(root, height=10, width=50)
code_display.pack()

# Text widget to display decoded text
decoded_display = tk.Text(root, height=10, width=50)
decoded_display.pack()

# Status label to show success or error messages
status_label = tk.Label(root, text="")
status_label.pack()

# Labels for file sizes and compression ratio
original_size_label = tk.Label(root, text="Original Size: 0 bytes")
original_size_label.pack()

compressed_size_label = tk.Label(root, text="Compressed Size: 0 bytes")
compressed_size_label.pack()

compression_ratio_label = tk.Label(root, text="Compression Ratio: 0.00%")
compression_ratio_label.pack()

root.mainloop()