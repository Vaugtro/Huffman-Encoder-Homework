
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

	def insert_root_node(self, node):
		if self.root is None:
			self.root = node
		else:
			return

	def inorder(self):
		if(self.root) is not None:
			self._inorder(self.root)
	
	def _inorder(self, node):
		global string_inorder
		if node is not None:
			self._inorder(node.left)
			string_inorder += (u"\u0000".join([node.symbol, str(node.frequency), str(node.code)])) + u'\u001F'
			self._inorder(node.right)

	def preorder(self):
		if(self.root) is not None:
			self._preorder(self.root)
	
	def _preorder(self, node):
		global string_preorder
		if node is not None:
			string_preorder += (u"\u0000".join([node.symbol, str(node.frequency), str(node.code)])) + u'\u001F'
			self._preorder(node.left)
			self._preorder(node.right)


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

	def __calculate_codes(self, node, value = ""):

		value = value + str(node.code)

		if(node.left):
			self.__calculate_codes(node.left, value)
		if(node.right):
			self.__calculate_codes(node.right, value)

		if(not node.left and not node.right):
			self.huffman_encoding[node.symbol] = value

	def __total_gain(self):
		uncompressed = len(self.content) * 8
		compressed = 0

		for symbol in self.huffman_encoding.keys():
			count = self.content.count(symbol)
			compressed += count * len(self.huffman_encoding[symbol])

		self.gains = {"uncompressed": uncompressed, "compressed": compressed}


	def __encode_output(self):
		output = []
		for c in self.content:
			output.append(self.huffman_encoding[c])

		self.encoded_content = self.__bitstring_to_bytes(''.join([str(item) for item in output]))

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

	def __string_to_btree(self, string):
		huffman_tree = BTree()

		for it in string:
			if(it[0] != ''):
				huffman_tree.insert(symbol = it[0], frequency = int(it[1]), code = it[2])

		self.huffman_tree = huffman_tree


	def decode(self, encoded_content):

		#self.__string_to_btree(string_tree)

		tree_head = self.huffman_tree.root
		btree = self.huffman_tree.root
		self.encoded_content = bin(int(binascii.hexlify(encoded_content), base=16)).lstrip('0b')
		#self.encoded_content = (''.join(format(x, 'b') for x in bytearray(str(encoded_content), 'utf-8')))

		del encoded_content

		decoded_content = []

		for it in self.encoded_content:
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

	def get_gains(self):
		return self.gains

	def get_content(self):
		return self.content

	def get_encode_content(self):
		return self.encoded_content

	def get_tree_str(self):
		global string_preorder

		string_preorder = ""
		self.huffman_tree.preorder()

		return string_preorder

	def get_tree(self):
		return self.huffman_tree

	def set_tree(self, huffman_tree):
		self.huffman_tree = huffman_tree