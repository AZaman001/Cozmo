import matplotlib.pyplot as plt
import numpy as np
import csv

labels=[]
values=[]
with open('result.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    result = list(readCSV)
    labels=result[0]
    values=result[1]
values=np.asarray(values)
values=values.astype(float)
values=values*100

fig, ax = plt.subplots()  
y_pos = np.arange(len(labels))

ax.bar(y_pos, values, align='center', alpha=0.5)
plt.xticks(y_pos, labels)
ax.set_ylim(0, 100)

for i, v in enumerate(values):
    plt.text(i - 0.2, v + 1, str(round(v,2))+ '%', color='blue', fontsize=14)

plt.ylabel('Percentage')
plt.title('Image Recognition')

plt.show(block=False)
plt.pause(3)
plt.close()