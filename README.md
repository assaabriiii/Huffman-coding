# Huffman Encoding and Decoding

This code demonstrates Huffman encoding and decoding for a given string.

## Introduction

The Huffman coding algorithm is a popular method for lossless data compression. It assigns variable-length codes to input characters based on their frequencies, with the more frequent characters having shorter codes. This allows for efficient encoding and decoding of data.

## Code Description

The code performs the following steps:

1. Defines the string to be encoded.
2. Defines the `NodeTree` class to represent nodes in the Huffman tree.
3. Defines the `huffman_code_tree` function to generate the Huffman tree and the corresponding code dictionary.
4. Calculates the frequencies of characters in the input string.
5. Builds the Huffman tree based on the frequencies.
6. Encodes the input string using the generated Huffman tree.
7. Decodes the encoded string using the Huffman tree.
8. Prints the original string, encoded string, and decoded string.

## Usage

To run the code, execute the `main()` function.

```python
if __name__ == '__main__':
    main()
