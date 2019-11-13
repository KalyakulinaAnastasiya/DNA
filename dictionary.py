import pickle
filename = "Dictionary(cpg - gene)"

dictionary = {}
cpg_str = []
gene_list = []
cpg_key = 'ID_REF'
gene_key = 'UCSC_REFGENE_NAME'
line_list = []
i = 0

file = open('annotations.txt', 'r')
line = file.readline().rstrip()
line_list = line.rstrip().split('\t')
cpg_id = line_list.index(cpg_key)
gene_id = line_list.index(gene_key)

for line in file:
    if line.find('cg') == 0:
        line_list = line.rstrip().split('\t')
        cpg_str = line_list[cpg_id]              #
        str = line_list[gene_id]
        if str.find(';') != (-1):
            gene_list = str.split(';')
        else:
            gene_list = [str]
        dictionary[cpg_str] = gene_list

'''while i < len(cpg_list):
    str = gene_list[i]
    if str.find(';') != (-1):
        line_list = str.split(';')
    dictionary[cpg_list[i]] = line_list
    i += 1'''


print(dictionary)
file.close()

with open(filename, "wb") as handle:
    pickle.dump(dictionary, handle, protocol = pickle.HIGHEST_PROTOCOL)


'''d = {}
file = open('annotations.txt', 'r')

cpg_key = 'ID_REF'
gene_key = 'UCSC_REFGENE_NAME'

line = file.readline().rstrip()              #читает и убирает /n
line_list = line.split('\t')                 #разбивает строку по заданному элементу(здесь пробел) и записывает в лист
cpg_id = line_list.index(cpg_key)
gene_id = line_list.index(gene_key)

cpg_list = []
gene_list = []

for line in file:
    line_list = line.rstrip().split('\t')

    cpg_list.append(line_list[cpg_id])

    gene_raw = line_list[gene_id]
    curr_gene_list = gene_raw.split(';')
    gene_list.append(list(set(curr_gene_list)))

a = 0

line = file.readable()
while line:
    print(line)
    line = file.readline()'''