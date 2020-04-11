import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

cpu_temp = pd.read_csv(r"temps", header=None)
cpu_temp.columns = ['Temperatura']
cpu_temp.Temperatura = cpu_temp.Temperatura *1/1000
cpu_temp.round(1)
plt.grid()
plt.axis([cpu_temp.index[0],max(list(cpu_temp.index)),0,100])
plt.plot(cpu_temp)
plt.savefig("static/cpu_temp_gr.png")