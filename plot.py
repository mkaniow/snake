import os, json
import numpy as np
import matplotlib.pyplot as plt


def Average(lst):
    return sum(lst) / len(lst)


def policz(path_to_json_files, liczba1, liczba2):
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

    rozmiar = []

    for item in json_file_names:
        holder = item[liczba1:liczba2]
        holder1 = []
        for i in holder:
            if i == '.':
                pass
            else:
                holder1.append(i)
        chwila = ''.join(holder1)
        chwila = int(chwila)
        rozmiar.append(chwila)
    
    zipped = zip(rozmiar, avrg, maxs)
    qwe1 = list(zipped)

    qwe2 = sorted(qwe1)

    avrg1 = []
    maxs1 = []
    rozmiar1 = []

    for i in qwe2:
        rozmiar1.append(i[0])
        avrg1.append(i[1])
        maxs1.append(i[2])

    return avrg1, maxs1, rozmiar1

srednia_double, max_double, rozmiar_double = policz('C:\\Users\\Michał\\Desktop\\repo\\snake\\poprawione_wyniki_deep_q_double', 17, 20)

srednia_double_BN, max_double_BN, rozmiar_double_BN = policz('C:\\Users\\Michał\\Desktop\\repo\\snake\\poprawione_wyniki_deep_q_double_BN', 20, 23)

srednia_double_DO, max_double_DO, rozmiar_double_DO = policz('C:\\Users\\Michał\\Desktop\\repo\\snake\\poprawione_wyniki_deep_q_double_DO', 20, 23)

srednia_jeden, max_jeden, rozmiar_jeden = policz('C:\\Users\\Michał\\Desktop\\repo\\snake\\wyniki_deep_q_double', 17, 20)

srednia_jeden_BN, max_jeden_BN, rozmiar_jeden_BN = policz('C:\\Users\\Michał\\Desktop\\repo\\snake\\wyniki_deep_q_BN', 20, 23)

srednia_jeden_DO, max_jeden_DO, rozmiar_jeden_DO = policz('C:\\Users\\Michał\\Desktop\\repo\\snake\\wyniki_deep_q_DO', 20, 23)

print(max_jeden)
print(max_jeden_BN)
print(max_jeden_DO)
print(max_double)
print(max_double_BN)
print(max_double_DO)

x_2 = [20, 35, 50, 65, 80, 95, 110, 125, 140, 155, 170, 185, 200, 215, 230]
x_3 = [20, 35, 50, 65, 80, 95, 110, 125, 140, 155, 170, 185, 200, 215]
x_4 = [20, 35, 50, 65, 80, 95, 110, 125, 140, 155, 200, 215, 230]
x_5 = [20, 50, 80, 110, 140, 170, 200, 230]

plt.figure()
plt.plot(rozmiar_jeden, srednia_jeden, label='jedna warstwa ukryta')
plt.plot(rozmiar_double, srednia_double, label='dwie warstwy ukryte')
plt.plot(rozmiar_jeden_BN, srednia_jeden_BN, label='jedna warstwa ukryta BN')
plt.plot(rozmiar_double_BN, srednia_double_BN, label='dwie warstwy ukryte BN')
plt.plot(rozmiar_jeden_DO, srednia_jeden_DO, label='jedna warstwa ukryta DO')
plt.plot(rozmiar_double_DO, srednia_double_DO, label='dwie warstwy ukryte DO')
plt.xlabel("Rozmiar warstwy", fontsize=20)
plt.ylabel("Średnia wyników", fontsize=20)
plt.yticks(fontsize=20)
plt.xticks(fontsize=20)
plt.legend(fontsize="20", loc ="upper left")

plt.figure()
plt.plot(rozmiar_jeden, max_jeden, label='jedna warstwa ukryta')
plt.plot(rozmiar_double, max_double, label='dwie warstwy ukryte')
plt.plot(rozmiar_jeden_BN, max_jeden_BN, label='jedna warstwa ukryta BN')
plt.plot(rozmiar_double_BN, max_double_BN, label='dwie warstwy ukryte BN')
plt.plot(rozmiar_jeden_DO, max_jeden_DO, label='jedna warstwa ukryta DO')
plt.plot(rozmiar_double_DO, max_double_DO, label='dwie warstwy ukryte DO')
plt.xlabel("Rozmiar warstwy", fontsize=20)
plt.ylabel("Maksymalny wynik", fontsize=20)
plt.yticks(fontsize=20)
plt.xticks(fontsize=20)
plt.legend(fontsize="20", loc ="upper left")

plt.show()