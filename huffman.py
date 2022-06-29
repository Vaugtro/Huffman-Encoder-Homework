
import binascii

# Nó de uma árvore de Huffman
class Node:

	# Inicializa nó da árvore
	def __init__(self, symbol, frequency, code = "", left = None, right = None):

		self.symbol = symbol
		self.frequency = frequency
		
		self.left = left
		self.right = right

		self.code = code

# Árvore Binária
class BTree:

	# Inicializa árvore binária
	def __init__(self, root = None):
		self.root = root

	# Inserção
	def insert(self, symbol, frequency, code):
		if self.root is None:
			self.root = Node(symbol, frequency, code)
		else:
			self._insert(symbol, frequency, self.root, code)

	# Inserção
	def _insert(self, symbol, frequency, node, code):
		if frequency < node.frequency:
			if node.left is not None:
				self._insert(symbol, frequency, node.left, code)
			else:
				node.left = Node(symbol, frequency, code)
		else:
			if node.right is not None:
				self._insert(symbol, frequency, node.right, code)
			else:
				node.right = Node(symbol, frequency, code)

	# Insere nó como nó raiz
	def insert_root_node(self, node):
		if self.root is None:
			self.root = node
		else:
			return


# Imprime a probabilidade dos símbolos em uma tabela

# Codificação com Huffman
class Huffman:

	# Inicializa codificação
	def __init__(self):
		self.content = None
		self.encoded_content = None

		self.symbols = dict()

		self.huffman_encoding = dict()

		self.gains = dict()

		self.huffman_tree = BTree()


	# Calcula a probabilidade dos símbolos
	def __calculate_probability(self):

		for el in self.content:
			if(self.symbols.get(el) == None):
				self.symbols[el] = 1
			else:
				self.symbols[el] += 1

	# Calcula os códigos
	def __calculate_codes(self, node, value = ""):

		value = value + str(node.code)

		if(node.left):
			self.__calculate_codes(node.left, value)
		if(node.right):
			self.__calculate_codes(node.right, value)

		if(not node.left and not node.right):
			self.huffman_encoding[node.symbol] = value

	# Ganho total de compressão em bits (Desconsiderando o preâmbulo)
	def __total_gain(self):
		uncompressed = len(self.content) * 8
		compressed = 0

		for symbol in self.huffman_encoding.keys():
			count = self.content.count(symbol)
			compressed += count * len(self.huffman_encoding[symbol])

		self.gains = {"uncompressed": uncompressed, "compressed": compressed}

	# Resultado da compressão e conversão para binário
	def __encode_output(self):
		output = []
		for c in self.content:
			output.append(self.huffman_encoding[c])

		self.encoded_content = self.__bitstring_to_bytes('1' + ''.join([str(item) for item in output]))

	# Conversão de string de bits para blob de bytes
	def __bitstring_to_bytes(self, value):
		return int(value, 2).to_bytes((len(value) + 7) // 8, byteorder='big')
		
	# Codificação com Huffman
	def encode(self, content):

		self.content = content

		self.__calculate_probability()

		# Inicializa fila de prioridade dos nós
		nodes = []

		# Converte símbolos e probabilidades em nós da árvore Huffman
		for key, value in self.symbols.items():
			nodes.append(Node(key, value))

		while len(nodes) > 1:
			nodes = sorted(nodes, key=lambda x: x.frequency)

			right = nodes[0]
			left = nodes[1]

			left.code = 0b0
			right.code = 0b1

			node = Node(left.symbol + right.symbol, left.frequency + right.frequency, left = left, right = right)

			nodes.remove(left)
			nodes.remove(right)
			nodes.append(node)
		
		# Inicializa árvore
		self.huffman_tree.insert_root_node(nodes[0])

		self.__calculate_codes(self.huffman_tree.root)
		self.__total_gain()
		self.__encode_output()

	# Decodificação com Huffman
	def decode(self, encoded_content):

		tree_head = self.huffman_tree.root
		btree = self.huffman_tree.root

		self.encoded_content = bin(int(binascii.hexlify(encoded_content), base=16)).lstrip('0b')

		decoded_content = []

		for it in self.encoded_content[1:]:
			if( it == '1'):
				btree = btree.right
			elif( it == '0'):
				btree = btree.left
			try:
				if btree.left.symbol == None and btree.right.symbol == None:
					pass
			except AttributeError:
				decoded_content.append(btree.symbol)
				btree = tree_head
			
		self.content = ''.join([str(it) for it in decoded_content])

	# Obter ganhos totais
	def get_gains(self):
		return self.gains

	# Obter conteúdo do texto
	def get_content(self):
		return self.content.encode("utf-8")

	# Obter conteúdo do texto codificado
	def get_encode_content(self):
		return self.encoded_content

	# Obter árvore de huffman
	def get_tree(self):
		return self.huffman_tree

	# Definir árvore de huffman
	def set_tree(self, huffman_tree):
		self.huffman_tree = huffman_tree