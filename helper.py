# -*- coding: utf-8 -*-
"""
Universidade Federal de Minas Gerais
Departamento de Ciência da Computação
Programa de Pós-Graduação em Ciência da Computação

Projeto e Análise de Algoritmos
Trabalho Prático de Grafos

Feito por Gabriel de Biasi, 2016672212.
"""

class Person(object):
	"""
	Esta classe representa os vértices do grafo.
	Seus meta dados são uma lista de arestas, a
	lista dos focos que pode visitar e seu ID.
	"""
	def __init__(self, id):
		self._friendship = []
		self._places = []
		self._id = id

	def __str__(self):
		return str(self._id)

	def __repr__(self):
		return self.__str__()

	def get_id(self):
		return self._id

	def get_places(self):
		return self._places

	def get_friendship(self):
		return self._friendship

	def add_place(self, place):
		self._places.append(place)

	def add_friend(self, friend):
		self._friendship.append(friend)


def union(l1, l2):
	return list(set(l1).union(l2))


def get_places_amount(graph):
	p = []
	for v in graph:
		p = union(p, v.get_places())
	return len(p)


def get_smaller_sum(final):
	# Calcula a soma de ids de todas as soluções.
	counter = []
	for graph in final:
		c = 0
		for v in graph:
			c += v.get_id()
		counter.append(c)

	# Verifica o índice da menor soma.
	smaller = counter[0]
	ind = 0
	for l in range(len(counter)):
		if smaller > counter[l]:
			ind = l
			smaller = counter[l]

	# Solução ótima :D
	return final[ind]

##
## Imprime a matriz de funções resumida
##
def print_use_table(M):
	v = 1
	print 'F',
	for i in range(1, len(M[0])+1):
		print (i%10),
	print '|'
	for l in M:
		print (v%10),
		v += 1
		for c in l:
			if len(c) > 0:
				print 'x',
			else:
				print ' ',
		print '|'
	for i in range(len(M[0])+2):
		print '=',
	print


##
## Combine Solution
##
def combine_solution(F, i, g1, g2):
	new = None
	t1, t2 = len(g1), len(g2)

	result = union(g1,g2)
	result.sort()
	tr = len(result)

	# Grafos de tamanhos diferentes
	# de (i+1) não importam.
	if tr != (i+1):
		return

	elif tr == t1 or tr == t2: # Tamanho igual: um era o subgrafo do outro.
		new = result
	else:
		for v1 in g1:
			for v2 in g2:
				if v1 in v2.get_friendship(): # Se achar pelo menos UMA relação, o grafo resultante é conexo.
					new = result
					break
			else:
				continue
			break

	# Grafo gerado não é conexo
	if new is None:
		return

	# Caso a combinação gere um subgrafo válido, a
	# quantidade de focos que ele visita (amount) é usado
	# para definir o índice de sua posição na matriz de 
	# soluções F.
	amount = get_places_amount(new)
	if new not in F[i][amount-1]:
		F[i][amount-1].append(new)


##
## Imprime a matriz de funções completa
##
def print_table(F, iteration):
	print '\n----------------------------------------------'
	for y in range(len(F[iteration])):
		print 'f(%d,%d)' % ((iteration+1),(y+1)), F[iteration][y]
	print
	print '----------------------------------------------'

class Problem(object):
	"""
	Classe para execução do problema.
	Após instanciada, pode ser executada
	várias vezes. pois o grafo original não
	é modificado.
	"""
	def __init__(self, persons, places, debug=False):
		self.persons = list(persons)
		self.amount_places = places
		self.DEBUG = debug

	def execute(self):

		# Cria a matriz de funções da programação dinâmica. O(V*R)
		F = []
		for j in range(len(self.persons)):
			F.append([])
			for k in range(self.amount_places):
				F[j].append([])

		# Inicializa a primeira linha de respostas da matriz, para 
		# cada vértice, é colocado na posição de quantidade de focos 
		# que ele visita sozinho, logo é considerado uma resposta 
		# ótima até o momento. O(v)
		for p in self.persons:
			pos = get_places_amount([p])
			if pos == self.amount_places: # Verificação de melhor caso.
				return [p]
			F[0][pos-1].append([p])

		if self.DEBUG:
			print_table(F, 0)

		# Laço de repetição principal
		# Cada linha e coluna representa uma lista de soluções com
		# no máximo (i) vértices e com no máximo (j) focos.
		for i in range(1, len(self.persons)):

			# Para cada lista de soluções de tamanho (i), é calculado
			# uma fusão dos subgrafos das soluções de tamanho (i-1) com no
			# máximo (j) focos em busca de novas soluções ótimas de 
			# tamanho >= i.
			for j in range(i-1, self.amount_places):

				# Há alguma solução na iteração anterior F(i-1,j) que possa ser
				# usado neste cálculo? Caso não haja, o processo de cálculo
				# é pulado pois não há nada à fazer.
				if len(F[i-1][j]) > 0:

					# Combinação interna da solução
					# anterior sem fazer repetições
					tam = len(F[i-1][j])
					for k in range(tam-1):
						for l in range(k+1, tam):
							combine_solution(F, i, F[i-1][j][k], F[i-1][j][l])

					# Cada solução em F(i-1,j) é usada para tentar combinar
					# com outras soluções de tamanho (i-1) que visitam (i...j)
					# focos de zica em busca de soluções que visitam uma quantidade
					# maior ou igual a (j).
					for y in range(i-1, j):

						# Processo de combinação de soluções de F(i-1,j) com
						# as soluções de F(i-1, y).
						for z in F[i-1][j]:
							for w in F[i-1][y]:
								combine_solution(F, i, z, w)

			# Verificação de Resposta #
			# Neste ponto, sempre (j==r). Portanto, se houver soluções
			# nesta posição da matriz, foi encontrada uma solução ótima.
			if len(F[i][j]) > 0:
				if self.DEBUG:
					print_table(F, i)
					print_use_table(F)
				return get_smaller_sum(F[i][j])

			# Para depuração #
			if self.DEBUG:
				print_table(F, i)

		# Caso inerperado!
		# Algo está muito errado se chegar aqui.
		return []