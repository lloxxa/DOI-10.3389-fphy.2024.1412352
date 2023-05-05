import glob
from turtle import position
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dir = r'C:\Users\Gebruiker\Documents\Uni dingen\Thesis\filmpjes-retractions'
pathlist = glob.glob(f'{dir}\*.csv')
fig,[ax1,ax2] = plt.subplots(2,1,sharex=True)
for i,path in enumerate(pathlist):
    if 'P4' in path:
        legend = ['Cup 1','Cup 2','Cup 3','Cup 4','Cup 5','Cup 6','Cup 7','Cup 8','Cup 9','Cup 10'] # dit is helemaal niet gebruteforced, hoe kom je erbij?
    elif 'P2.5' in path:
        legend = ['Cup 1','Cup 2','Cup 3','Cup 4','Cup 5','Cup 6','Cup 7','Cup 8','Cup 9','Cup 10','Cup 11']
    df = pd.read_csv(path,delimiter=';',decimal=',')
    for j,row in df.iterrows():
        row = list(float(order) for order in row)
        data = {int(j+1):row}
        if i==0:
            ax1.plot(np.arange(len(data[j+1])),data[j+1])
            ax1.legend(labels=legend,loc='center left', bbox_to_anchor=(1, 0.5))
        elif i==1:
            ax2.plot(np.arange(len(data[j+1])),data[j+1])
fig.supxlabel('Measurement number')
fig.supylabel('Detachment order')
plt.tight_layout()
plt.show()
