import matplotlib.pyplot as plt
import numpy as np
import csv

with open('results.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))[1:]

print(data)

fig, ax = plt.subplots(1, 1, layout="constrained")
fig2, ax2 = plt.subplots(1, 1, layout="constrained")
fig3, ax3 = plt.subplots(1, 1, layout="constrained")

ax.bar([x[0] for x in data], [float(x[1][:-2]) for x in data])
ax.tick_params("x", rotation=90)

ax.set_xlabel("Test Names")
ax.set_ylabel("Metadata Sizes in Bytes")

ax2.bar([x[0] for x in data], [float(x[2]) / 100.0 for x in data])
ax2.tick_params("x", rotation=90)
ax2.set_xlabel("Test Names")
ax2.set_ylabel("Metadata Size compared to Bytecode")
ax2.yaxis.set_major_formatter('{x}x')


ax3.bar([x[0] for x in data], [float(x[3]) for x in data])
ax3.tick_params("x", rotation=90)
ax3.set_xlabel("Test Names")
ax3.set_ylabel("% of Binary Occupied By Metadata")

fig.savefig("figure.png")
fig2.savefig("figure2.png")
fig3.savefig("figure3.png")