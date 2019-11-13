import pickle
import numpy as np


file = open('betas.txt', 'r')
line = file.readline()                                    #пропускаем первую строку
line_list = line.rstrip().split('\t')

num_cols = len(line_list) - 1                             #кол-во столбцов

num_rows = 0                                              #кол-во строк
cpg_row_dict = {}                                         #словарь cpg-номер строки
for line in file:
    line_list = line.rstrip().split('\t')
    cpg_row_dict[line_list[0]] = num_rows
    num_rows += 1
file.close()

betas = np.zeros((num_rows, num_cols), dtype=float32)    #матрицв с внутренними данными
file = open('betas.txt', 'r')
file.readline()

curr_row = 0                                             #номер строки внутри
for line in file:
    line_list = line.rstrip().split('\t')
    curr_betas = float(line_list[1::])
    betas[curr_row, :] = curr_betas
    curr_row += 1
file.close()

with open('gene_cpg_dict.pkl', 'rb') as handle:          #словарь ген-cpg
    gene_cpg_dict = pickle.load(handle)

genes = np.zeros(shape=(len(gene_cpg_dict), num_cols), dtype=float32)  #матрицв средних cpg для генов
gene_row_dict = {}                                                     #словарь ген-номер строки
curr_row = 0
for gene, cpg_list in gene_cpg_dict.items():
    gene_row_dict[gene] = curr_row
    curr_gene_betas = np.zeros(shape=(1, num_cols))                    #матрица со значениями cpg для гена
    for cpg in cpg_list:
        cpg_row = cpg_row_dict[cpg]
        curr_cpg_betas = betas[cpg_row, :]
        curr_gene_betas += curr_cpg_betas
    curr_gene_betas /= float(len(cpg_list))
    genes[curr_row, :] = curr_gene_betas


