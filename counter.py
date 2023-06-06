import os, json
import numpy as np
import matplotlib.pyplot as plt


def Average(lst):
    return sum(lst) / len(lst)



path_to_json_files = 'C:\\Users\\Michał\\Desktop\\repo\\snake\\wyniki_q-learning'
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

x = np.outer(np.linspace(0.1, 0.9, 9), np.ones(9))
y = x.copy().T

X = np.arange(0.1, 1, 0.1)
Y = np.arange(0.1, 1, 0.1)

X1 = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9']

average = []
maximum = []
mediana = []

i = 0
j = 0
for item in avrg:
    if i % 9 == 0:
        average.append(list())
        j += 1
    i += 1
    average[j-1].append(item)

i = 0
j = 0
for item in maxs:
    if i % 9 == 0:
        maximum.append(list())
        j += 1
    i += 1
    maximum[j-1].append(item)

i = 0
j = 0
for item in median:
    if i % 9 == 0:
        mediana.append(list())
        j += 1
    i += 1
    mediana[j-1].append(item)

zxc = np.array(average)
xcv = np.array(maximum)
cvb = np.array(mediana)

for i in range(len(zxc)):
    for j in range(len(zxc[0])):
        zxc[i, j] = round(zxc[i, j], 2)


fig, ax = plt.subplots()
im = ax.imshow(zxc)
ax.set_xticks(np.arange(len(X)), labels=X1)
ax.set_yticks(np.arange(len(Y)), labels=X1)

for i in range(len(X)):
    for j in range(len(Y)):
        text = ax.text(j, i, zxc[i, j],
                       ha="center", va="center", color="w")

ax.set_title("Średnia wyników z gier")
plt.xlabel("alfa")
plt.ylabel("gamma")

cbar = ax.figure.colorbar(im, ax = ax)
cbar.ax.set_ylabel("", rotation = -90, va = "bottom")


fig, ax = plt.subplots()
im = ax.imshow(xcv)
ax.set_xticks(np.arange(len(X)), labels=X1)
ax.set_yticks(np.arange(len(Y)), labels=X1)

for i in range(len(X)):
    for j in range(len(Y)):
        text = ax.text(j, i, xcv[i, j],
                       ha="center", va="center", color="w")

ax.set_title("Najwyższe wyniki z gier")
plt.xlabel("alfa")
plt.ylabel("gamma")

cbar = ax.figure.colorbar(im, ax = ax)
cbar.ax.set_ylabel("", rotation = -90, va = "bottom")

fig, ax = plt.subplots()
im = ax.imshow(cvb)
ax.set_xticks(np.arange(len(X)), labels=X1)
ax.set_yticks(np.arange(len(Y)), labels=X1)

for i in range(len(X)):
    for j in range(len(Y)):
        text = ax.text(j, i, cvb[i, j],
                       ha="center", va="center", color="w")

ax.set_title("Mediana wyników z gier")
plt.xlabel("alfa")
plt.ylabel("gamma")

cbar = ax.figure.colorbar(im, ax = ax)
cbar.ax.set_ylabel("", rotation = -90, va = "bottom")

plt.show()
