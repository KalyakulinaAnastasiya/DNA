import numpy as np
#import statsmodels.api as sm
import pickle
import math
import statsmodels.api as sm
'''import matplotlib.pyplot as plt
import openpyxl
from openpyxl import Workbook
from openpyxl import load_workbook
import os'''
import xlsxwriter

file = open('D:\Kalyakulina_Anastasiya\OLS\observables.txt', 'r')
age_key = 'age'
#pers_key = 'geo_accession'
gender_key = 'gender'

line = file.readline().rstrip()
line_list = line.split('\t')
#pers_id = line_list.index(pers_key)
age_id = line_list.index(age_key)
gender_id = line_list.index(gender_key)
line_age = []
line_m = []
line_f = []
age_m = []
age_f = []

i = 0
for line in file:
    line_list = line.rstrip().split('\t')
    line_age.append(int(line_list[age_id]))
    if line_list[gender_id] == 'M':
        line_m.append(i)
    else:
        line_f.append(i)
    i += 1
file.close()

for i in line_m:
    age_m.append(line_age[i])
for i in line_f:
    age_f.append(line_age[i])

with open('D:\Kalyakulina_Anastasiya\OLS\gene_row', 'rb') as handle:
    gene_row = pickle.load(handle)
    #gene_id = gene_row['ELOVL2']

name = []
I = []
R_m = []
R_f = []
data = np.load('D:\Kalyakulina_Anastasiya\OLS\gene_npz.txt.npz')
betas = data['arr_0']
for gene_name in gene_row.keys():
    gene_id = gene_row[gene_name]
    name.append(gene_name)

    cpg_betas = betas[gene_id]
    betas_m = []
    betas_f = []
    for i in line_m:
        betas_m.append(cpg_betas[i])
    for i in line_f:
        betas_f.append(cpg_betas[i])

    X = sm.add_constant(age_m)
    model = sm.OLS(betas_m, X)
    results = model.fit()
    R_m.append(results.rsquared)

    X = sm.add_constant(age_f)
    model = sm.OLS(betas_f, X)
    results = model.fit()
    R_f.append(results.rsquared)

    x_min = min(line_age)
    x_max = max(line_age)
    y_min = min(cpg_betas)
    y_max = max(cpg_betas)
    age = 10
    bet = 10
    h_x = (max(line_age) - min(line_age) + 10**(-12))/age
    h_y = (max(cpg_betas) - min(cpg_betas) + 10**(-12))/bet
    eps = 10**(-12)
    mark_x_m = []
    mark_y_m = []
    mark_x_f = []
    mark_y_f = []
    for temp in age_m:
        #id_x = (age*(temp - x_min)/((x_max - x_min) + eps)) + 1
        id_x = ((temp - x_min) / h_x)
        id_x = math.floor(id_x)
        mark_x_m.append(id_x)
    for temp in age_f:
        #id_x = (age*(temp - x_min)/((x_max - x_min) + eps)) + 1
        id_x = ((temp - x_min) / h_x)
        id_x = math.floor(id_x)
        mark_x_f.append(id_x)
    for temp in betas_m:
        #id_y = (bet*(temp - y_min)/((y_max - y_min) + eps)) + 1
        id_y = ((temp - y_min)/h_y)
        id_y = math.floor(id_y)
        mark_y_m.append(id_y)
    for temp in betas_f:
        #id_y = (bet*(temp - y_min)/((y_max - y_min) + eps)) + 1
        id_y = ((temp - y_min) / h_y)
        id_y = math.floor(id_y)
        mark_y_f.append(id_y)

    male = np.zeros((10, 10), dtype=int)
    female = np.zeros((10, 10), dtype=int)

    for temp1, temp2 in zip(mark_x_m, mark_y_m):
        male[temp1, temp2] += 1
    for temp1, temp2 in zip(mark_x_f, mark_y_f):
        female[temp1, temp2] += 1

    i = 0
    j = 0
    s = 0
    while i < 10:
        j = 0
        while j < 10:
            s += min(female[i][j], male[i][j])
            j += 1
        i += 1
    I.append(s)

'''space_x = np.linspace(x_min, x_max, 20)
space_y = np.linspace(y_min, y_max, 30)
biggi = male + female
print(biggi)
print(len(space_x))
print(len(space_y))'''

workbook = xlsxwriter.Workbook('PDF.xlsx')
worksheet = workbook.add_worksheet()
line = ['Genes', 'I', 'R_m', 'R_f']
i = 0
for elem in line:
    worksheet.write(0, i, elem)
    i += 1
i = 1
for temp1, temp2, temp3, temp4 in zip(name, I, R_m, R_f):
    worksheet.write(i, 0, temp1)
    worksheet.write(i, 1, temp2)
    worksheet.write(i, 2, temp3)
    worksheet.write(i, 3, temp4)
    i += 1

workbook.close()
#cc = plt.hist2d(space_x, space_y, biggi, alpha=1)
#cbar = plt.colorbar(cc)
#plt.show()

#print(s)
#print(male)
'''print(len(mark_x_m))
print(len(mark_y_m))
print(len(mark_x_f))
print(len(mark_y_f))'''
'''X = sm.add_constant(age_m)
model = sm.OLS(betas_m, X)
results_m = model.fit()
Y = sm.add_constant(age_f)
model = sm.OLS(betas_f, Y)
results_f = model.fit()
plt.scatter(age_m, betas_m, label='', color='c', s=8)
plt.scatter(age_f, betas_f, label='', color='m', s=8)
plt.plot(X, results_m.predict(X), color='blue', linewidth=2)
plt.plot(Y, results_f.predict(Y), color='red', linewidth=2)
plt.title('ELOVL2')
plt.xlabel('age')
plt.ylabel('betas')
plt.show()'''