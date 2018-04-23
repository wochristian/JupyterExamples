from vpython import *

# Histogram Demo
# Wolfgang Cristian

graphHeight = 200  # histogram width
graphWidth = 400   # histogram height

binsize = 0.1  # histogram bin width
nhisto = int(4 / binsize)   # number of histograms
histo = []

for i in range(nhisto):  # Initialize historgram data
    histo.append(0)

s = """Random Number Distribution"""
graph(title=s, width=graphWidth, height=graphHeight, xmax=1, ymax=10, align='left')

accum = []
for i in range(int(1 / binsize)):
    accum.append([binsize * (i + .5), 5*random()])

dist = gvbars(color=color.red, delta=binsize)
dist.data = accum
