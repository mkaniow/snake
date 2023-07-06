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

for json_file_name in json_file_names:
    with open(os.path.join(path_to_json_files, json_file_name)) as json_file:
        json_text = json.load(json_file)
        qwe = json_text["score"]
        asd = qwe[150::]
        average = Average(asd)
        maximum = max(asd)
        avrg.append(average)
        maxs.append(maximum)

x_2 = [20, 35, 50, 65, 80, 95, 110, 125, 140, 155, 170, 185, 200, 215, 230]
x_3 = [20, 35, 50, 65, 80, 95, 110, 125, 140, 155, 170, 185, 200, 215]
x_4 = [20, 35, 50, 65, 80, 95, 110, 125, 140, 155, 200, 215, 230]

path_to_json_files = 'C:\\Users\\Michał\\Desktop\\repo\\snake\\wyniki_deep_q_double'
#get all JSON file names as a list
json_file_names = [filename for filename in os.listdir(path_to_json_files) if filename.endswith('.json')]

avrg_double = []
maxs_double = []

for json_file_name in json_file_names:
    with open(os.path.join(path_to_json_files, json_file_name)) as json_file:
        json_text = json.load(json_file)
        qwe = json_text["score"]
        asd = qwe[150::]
        average = Average(asd)
        maximum = max(asd)
        avrg_double.append(average)
        maxs_double.append(maximum)

path_to_json_files = 'C:\\Users\\Michał\\Desktop\\repo\\snake\\wyniki_deep_q_BN'
#get all JSON file names as a list
json_file_names = [filename for filename in os.listdir(path_to_json_files) if filename.endswith('.json')]

avrg_BN = []
maxs_BN = []

for json_file_name in json_file_names:
    with open(os.path.join(path_to_json_files, json_file_name)) as json_file:
        json_text = json.load(json_file)
        qwe = json_text["score"]
        asd = qwe[150::]
        average = Average(asd)
        maximum = max(asd)
        avrg_BN.append(average)
        maxs_BN.append(maximum)

path_to_json_files = 'C:\\Users\\Michał\\Desktop\\repo\\snake\\wyniki_deep_q_DO'
#get all JSON file names as a list
json_file_names = [filename for filename in os.listdir(path_to_json_files) if filename.endswith('.json')]

avrg_DO = []
maxs_DO = []

for json_file_name in json_file_names:
    with open(os.path.join(path_to_json_files, json_file_name)) as json_file:
        json_text = json.load(json_file)
        qwe = json_text["score"]
        asd = qwe[150::]
        average = Average(asd)
        maximum = max(asd)
        avrg_DO.append(average)
        maxs_DO.append(maximum)

plt.figure()
plt.plot(x_2, avrg, label='jeden')
plt.plot(x_2, avrg_double, label='dwa')
plt.plot(x_4, avrg_BN, label='BN')
plt.plot(x_3, avrg_DO, label='DO')
plt.xlabel("Liczba gier")
plt.ylabel("Średnia wyników")

plt.figure()
plt.plot(x_2, maxs, label='jeden')
plt.plot(x_2, maxs_double, label='dwa')
plt.plot(x_4, maxs_BN, label='BN')
plt.plot(x_3, maxs_DO, label='DO')
plt.xlabel("Liczba gier")
plt.ylabel("Maksymalny wynik")

plt.show()