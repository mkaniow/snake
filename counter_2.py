import os, json
import numpy as np
import matplotlib.pyplot as plt


def Average(lst):
    return sum(lst) / len(lst)



path_to_json_files = 'C:\\Users\\Michał\\Desktop\\repo\\snake\\wyniki_deep_q'
#get all JSON file names as a list
json_file_names = [filename for filename in os.listdir(path_to_json_files) if filename.endswith('.json')]

avrg = []
maxs = []
median = []

for json_file_name in json_file_names:
    with open(os.path.join(path_to_json_files, json_file_name)) as json_file:
        json_text = json.load(json_file)
        qwe = json_text["score"]
        asd = qwe[150::]
        average = Average(asd)
        maximum = max(asd)
        asd.sort()
        mid = len(asd) // 2
        res = (asd[mid] + asd[~mid]) / 2
        avrg.append(average)
        maxs.append(maximum)
        median.append(res)

x_2 = [20, 35, 50, 65, 80, 95, 110, 125, 140, 155, 170, 185, 200, 215, 230]
print(avrg)

path_to_json_files = 'C:\\Users\\Michał\\Desktop\\repo\\snake\\wyniki_deep_q_double'
#get all JSON file names as a list
json_file_names = [filename for filename in os.listdir(path_to_json_files) if filename.endswith('.json')]

avrg_double = []
maxs_double = []
median_double = []

for json_file_name in json_file_names:
    with open(os.path.join(path_to_json_files, json_file_name)) as json_file:
        json_text = json.load(json_file)
        qwe = json_text["score"]
        asd = qwe[150::]
        average = Average(asd)
        maximum = max(asd)
        asd.sort()
        mid = len(asd) // 2
        res = (asd[mid] + asd[~mid]) / 2
        avrg_double.append(average)
        maxs_double.append(maximum)
        median_double.append(res)

print(avrg_double)

plt.figure()
plt.plot(x_2, avrg, label='jeden')
plt.plot(x_2, avrg_double, label='dwa')
plt.legend()
plt.title('średnia')

plt.figure()
plt.plot(x_2, maxs, label='jeden')
plt.plot(x_2, maxs_double, label='dwa')
plt.legend()
plt.title('najwyższy wynik')

plt.figure()
plt.plot(x_2, median, label='jeden')
plt.plot(x_2, median_double, label='dwa')
plt.legend()
plt.title('mediana')


plt.show()