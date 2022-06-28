import os
import re
import huffman
import pickle

def encode():

	with open('file.txt', encoding='utf-8') as f:
		content = f.read()
	
	huffman_obj = huffman.Huffman()
	huffman_obj.encode(content)

	with open('file.zin', 'wb') as f:
		#f.write((u"huffman/zin" + str(huffman_obj.get_tree_str()) + "huffman/zin").encode("utf-8"))
		pickle.dump(huffman_obj.get_tree(), f)
		f.write(huffman_obj.get_encode_content())

def decode():
	with open('file.zin', "rb") as f:
		test = pickle.load(f)
		content = f.read()
	content = content.decode("utf-8", errors="ignore")
	#string_tree = re.search(r"huffman/zin([\s\S]*?)huffman/zin", content).group(1)
	content = content.replace("huffman/zin" + string_tree + "huffman/zin", "")

	string_tree = string_tree.split(u"\u001F")

	for count, value in enumerate(string_tree):
		string_tree[count] = value.split(u"\u0000")

	huffman_obj = huffman.Huffman()
	huffman_obj.decode(content, string_tree)
	poop = huffman_obj.get_content()
	print()

encode()
decode()