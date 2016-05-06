# -*- coding: utf-8 -*-
"""
Universidade Federal de Minas Gerais
Departamento de Ciência da Computação
Programa de Pós-Graduação em Ciência da Computação

Projeto e Análise de Algoritmos
Trabalho Prático de Grafos

Feito por Gabriel de Biasi, 2016672212.
"""

# Você entendeu :)
DEBUG = False
SHUFFLE = False

import re, sys
from timeit import default_timer as timer
from helper import Person, Problem

def line_to_list(string):
	return [int(x) for x in re.findall('\d+', string)]

if __name__ == '__main__':

	# Teste de parâmetro.
	if len(sys.argv) != 3:
		print 'fail'
		exit()

	# Abertura dos arquivos.
	try:
		data = open(sys.argv[1], 'r')
		out = open(sys.argv[2], 'w')
	except:
		print 'fail on open file'
		exit()

	# Obtem os valores N e M.
	li = line_to_list(data.readline())
	n, m = li[0], li[1]

	# Cria a lista de vértices, no caso lista de 
	# instância de Persons e suas relações.
	persons = [Person(x) for x in range(1, n+1)]
	for i in range(m):
		li = line_to_list(data.readline())
		persons[li[0]-1].add_friend(persons[li[1]-1])
		persons[li[1]-1].add_friend(persons[li[0]-1])

	# Obtem o valor de R.
	r = int(data.readline())

	# Realiza o mapeamento da função R(v) para 
	# cada vértice do grafo.
	for i in range(n):
		li = line_to_list(data.readline())
		for j in li:
			persons[i].add_place(j)

	# Fecha o arquivo de entrada de dados.
	data.close()

	# Permutar as posições dos vértices na lista, 
	# se necessário por algum motivo.
	if SHUFFLE:
		from random import shuffle
		shuffle(persons)

	# Visualização de grafo gerado (para depuração).
	if DEBUG:
		print '---'
		for i in range(n):
			print persons[i], '>',
			for j in persons[i].get_friendship():
				print j,
			print persons[i].get_places()
		print '---'

	# Cria a instância do problema.
	p = Problem(persons, r, DEBUG)

	# Execução e cálculo de tempo gasto.
	start_time = timer()
	result = p.execute()
	end_time = timer()

	# Escrita da resposta no arquivo de saída
	for i in result:
		out.write(str(i)+' ')
	out.write('\n')
	out.close()

	if DEBUG:
		print '(',
		for i in result:
			print i, 
		print ')\nV = %d E = %d R = %d S = %s (N: %d) (I: %d) (TIME: %f)' % (n, m, r, len(result), p.calls, p.in_calls, end_time-start_time)
