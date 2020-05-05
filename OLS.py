import numpy as np
import statsmodels.api as sm
import pickle
import matplotlib.pyplot as plt
import openpyxl
from openpyxl import Workbook
from openpyxl import load_workbook
import os
import xlsxwriter

gene_cpg_dict = {}
with open('Optimal_dict_gene-cpgs.txt') as inp:
    for line in inp:
        key, val = line.split(': ')
        list = val.rstrip().split(' ')
        gene_cpg_dict[key] = list

cpg_chr = {}
file = open('annotations.txt', 'r')
cpg_key = 'ID_REF'
chr_key = 'CHR'
line = file.readline().rstrip()
line_list = line.rstrip().split('\t')
cpg_id = line_list.index(cpg_key)
chr_id = line_list.index(chr_key)
for line in file:
    line_list = line.rstrip().split('\t')
    cpg_chr[line_list[cpg_id]] = line_list[chr_id]
file.close()

pers_age = {}
file = open('observables.txt', 'r')
age_key = 'age'
pers_key = 'geo_accession'

line = file.readline().rstrip()
line_list = line.split('\t')
pers_id = line_list.index(pers_key)
age_id = line_list.index(age_key)
line_age = []  #int age

for line in file:
    line_list = line.rstrip().split('\t')
    pers_age[line_list[pers_id]] = line_list[age_id]  #словарь человек-возраст
    line_age.append(int(line_list[age_id]))

file.close()

data = np.load('gene_npz.txt.npz')
betas = data['arr_0']

with open('gene_row', 'rb') as handle:
    gene_num = pickle.load(handle)

workbook = xlsxwriter.Workbook('OLS.xlsx')
worksheet = workbook.add_worksheet()

line = ['Genes', 'Chromosome','R-squared', 'Adj. r-squared', 'F-statistic', 'Prob(F-statistic)', 'Intercept', 'Intercept std err', 'Slope', 'Slope std err']
i = 0
for elem in line:
    worksheet.write(0, i, elem)
    i += 1

j = 1
cpg_betas = []  #список значений cpg
list_r2 = []
list_data = []
for gene_name in gene_cpg_dict.keys():
    num = gene_num[gene_name]
    cpg_betas = betas[num, :]
   # if gene_name == 'FHL2':
    #    deb = 1
    X = sm.add_constant(line_age)
    model = sm.OLS(cpg_betas, X)
    results = model.fit()  #оптимальные a, b
    cpg = gene_cpg_dict[gene_name]
    chr = cpg_chr[cpg[0]]
    list_r2.append(results.rsquared)
    line = [gene_name, chr, results.rsquared_adj, results.fvalue, results.f_pvalue, results.params[0], results.bse[0], results.params[1], results.bse[1]]
    list_data.append(line)

list_r2.sort(reverse=True)
print(list_r2)
i = 0
j = 1
while i < len(list_r2):
    elem1 = list_r2[i]
    elem2 = list_data[i]
    i += 1
    worksheet.write(j, 2, elem1)
    k = 0
    for elem3 in elem2:
        worksheet.write(j, k, elem3)
        if k == 1:
            k += 2
        else:
            k += 1
    j += 1

workbook.close()

