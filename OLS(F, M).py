import numpy as np
import statsmodels.api as sm
import pickle
import matplotlib.pyplot as plt

file = open('observables.txt', 'r')
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

with open('gene_row', 'rb') as handle:
    gene_row = pickle.load(handle)
    gene_id = gene_row['ELOVL2']

data = np.load('gene_npz.txt.npz')
betas = data['arr_0']
cpg_betas = betas[gene_id]
betas_m = []
betas_f = []
for i in line_m:
    betas_m.append(cpg_betas[i])
for i in line_f:
    betas_f.append(cpg_betas[i])

X = sm.add_constant(age_m)
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
plt.show()