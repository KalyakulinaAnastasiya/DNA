import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
import numpy as np
from scipy import interpolate

file = open('D:\Kalyakulina_Anastasiya\OLS\observables.txt')
key_age = 'age'
key_sex = 'gender'
line = file.readline().rstrip()
list = line.split('\t')
id_age = list.index(key_age)
id_sex = list.index(key_sex)
list_age_m = []
list_age_f = []
list_age = []
for line in file:
    line_list = line.rstrip().split('\t')
    list_age.append(int(line_list[id_age]))
    if line_list[id_sex] == 'M':
        list_age_m.append(int(line_list[id_age]))
    else:
        list_age_f.append(int(line_list[id_age]))
file.close()
list_age.sort()
list_age_f.sort()
list_age_m.sort()

i = 0
amount = [0]
new_temp = min(list_age)
new_age = [min(list_age)]
#new_age = []
l = len(list_age)
for temp in list_age:
    if temp == new_temp:
        amount[i] += 1
    else:
        amount.append(1)
        new_age.append(temp)
        new_temp = temp
        amount[i] /= (l*4)
        i += 1
amount[i] /= (l*4)
max_elem = max(list_age)
min_elem = min(list_age)

space = np.linspace(min_elem, max_elem, 21)
x = np.array(new_age)
y = np.array(amount)

f = interpolate.interp1d(x, y, kind='quadratic')
y_new = f(space)
#print(y_new)
print(f)
#plt.plot(new_age, amount, color='green')
plt.plot(space, y_new)
#plt.scatter(x, y, label='', color='green', s=8)
plt.xticks(space)
plt.title('PDF')
plt.xlabel('x')
plt.ylabel('P(x)')
#plt.savefig('D:\Kalyakulina_Anastasiya\Higstogram\PDF(age).pdf')
plt.show()


plt.hist(list_age, space, edgecolor='black', color='orange')
plt.xticks(space)
plt.title('Age distribution')
plt.xlabel('Age')
plt.ylabel('Number of patients')
plt.savefig('D:\Kalyakulina_Anastasiya\Higstogram\Higstogram.pdf')
plt.show()


plt.hist(list_age_m, space, alpha=0.5, edgecolor='black', color='blue', label='man')
plt.hist(list_age_f, space, alpha=0.5, edgecolor='black', color='purple', label='women')
plt.xticks(space)
plt.title('Age distribution')
plt.xlabel('Age')
plt.ylabel('Number of patients')
plt.legend(loc='upper right')
#plt.savefig('D:\Kalyakulina_Anastasiya\Higstogram\Hist_f_m.pdf')
plt.show()

