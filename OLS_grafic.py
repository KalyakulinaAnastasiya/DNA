import numpy as np
import statsmodels.api as sm
import pickle
import matplotlib.pyplot as plt
import openpyxl
from openpyxl import Workbook
from openpyxl import load_workbook
import os
import xlsxwriter

top_list = ['ELOVL2', 'F5', 'NWD1', 'KLF14', 'MIR935', 'FAM181B', 'ZAR1', 'ZIC1', 'CCDC102B']

#pers_age = {}
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
    #pers_age[line_list[pers_id]] = line_list[age_id]  #словарь человек-возраст
    line_age.append(int(line_list[age_id]))

file.close()

with open('gene_row', 'rb') as handle:
    gene_num = pickle.load(handle)

data = np.load('gene_npz.txt.npz')
betas = data['arr_0']

for elem in top_list:
    num = gene_num[elem]
    cpg_betas = betas[num]
    X = sm.add_constant(line_age)
    model = sm.OLS(cpg_betas, X)
    results = model.fit()
    plt.scatter(line_age, cpg_betas, label='', color='k', s=8)
    plt.plot(X, results.predict(X), color='red', linewidth=2)
    plt.title(elem)
    plt.xlabel('age')
    plt.ylabel('betas')
    plt.show()

