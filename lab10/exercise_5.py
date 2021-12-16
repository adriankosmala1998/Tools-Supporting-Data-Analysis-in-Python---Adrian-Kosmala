import numpy as np

#load data
data = np.load('data/sample_treated.npz')
outputs = data['outputs']

#save shape of array - will be used later in loop
nr_rows = outputs.shape[0]
nr_columns = outputs.shape[1]

#create empty list - loop will be appending size growth there
growth_list = list()

for row in range(nr_rows):
    start_size = outputs[row, 0]
    end_size = outputs[row, nr_columns-1]
    size_growth = end_size/start_size
    growth_list.append(size_growth)

#print number of observations that doubled
print('Objects number:')
for i in range(len(growth_list)):
    if round(growth_list[i],1) == 2:
        print(i)

print('doubled their size during observation.')
print('Precision: one decimal place.')

