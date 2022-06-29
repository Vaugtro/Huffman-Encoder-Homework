import os
import huffman
import pickle

# Executa codificação
def encode():

	with open('file.txt', encoding='utf-8') as f:
		content = f.read()
	
	huffman_obj = huffman.Huffman()
	huffman_obj.encode(content)
	poop = huffman_obj.get_encode_content()

	with open('encode.zin', 'wb') as f:
		pickle.dump(huffman_obj.get_tree(), f)
		f.write(huffman_obj.get_encode_content())

# Executa decodificação
def decode():

	huffman_obj = huffman.Huffman()

	with open('encode.zin', "rb") as f:
		huffman_obj.set_tree(pickle.load(f))
		content = f.read()
	huffman_obj.decode(content)

	with open('decode.txt', 'wb') as f:
		f.write(huffman_obj.get_content())

encode()
decode()