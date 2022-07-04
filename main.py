import os
import huffman
import pickle
import pandas as pd

# Executa codificação
def encode():

	with open('file.txt', encoding='utf-8') as f:
		content = f.read()
	
	huffman_obj = huffman.Huffman()
	huffman_obj.encode(content)
	
	gains = huffman_obj.get_gains()
	table = huffman_obj.get_table()

	print(f"Arquivo decodificado em Bytes (Sem preâmbulo): {gains['uncompressed']}")
	print(f"Arquivo codificado em Bytes (Sem preâmbulo): {gains['compressed']}")
	print(f"Taxa de compressão (Sem preâmbulo): {(gains['compressed'] / gains['uncompressed']) * 100}%")

	# Utilização da biblioteca pandas para facilitar a construção do CSV
	df = pd.DataFrame.from_records(table)
	df.to_csv('results/out.csv')

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

# Imprime a taxa de compressão dos arquivos
def file_compress_ratio():
	if(os.path.exists("file.txt") and os.path.exists("encode.zin")):

		decode_stats = os.stat("decode.txt")
		encode_stats = os.stat("encode.zin")

		print(f"Arquivo decodificado em Bytes: {decode_stats.st_size}")
		print(f"Arquivo codificado em Bytes: {encode_stats.st_size}")
		print(f"Taxa de compressão: {(encode_stats.st_size / decode_stats.st_size) * 100}%")

encode()
decode()

file_compress_ratio()