import matplotlib.pyplot as plt
import numpy as np
from math import pi

diams = [2, 5.7, 7.3, 8.7, 10., 11.5, 12.8, 14., 15., 16.]
nodeNodeSep = [320, 500, 760, 1000, 1150, 1250, 1350, 1400, 1450, 1500]
noLamella = [30, 80, 100, 110, 120, 130, 135, 140, 145, 150]
nodeDiam = [1.4, 1.9, 2.4, 2.8, 3.3, 3.7, 4.2, 4.7, 5., 5.5]
MYSADiam = nodeDiam
FLUTLen = [10, 35, 38, 40, 46, 50, 54, 56, 58, 60]
FLUTDiam = [1.6, 3.4, 4.6, 5.8, 6.9, 8.1, 9.2, 10.4, 11.5, 12.7]
STINLen = [57.7, 70.5, 111.2, 152.2, 175.2, 190.5, 205.8, 213.5, 221.2, 228.8]
STIDiam = FLUTDiam

nodeLen = 3
densityNaChannels = 1 # insert correct here

diamArray = np.arange(0.1, 20, 0.1)

# f, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2,3)

startIndexFit = 0

# ax1.scatter(diams, nodeNodeSep, label='Node Separation')
# ax1.set_title('Node Separation')
z1 = np.polyfit(diams[startIndexFit:], nodeNodeSep[startIndexFit:], 1)
p1 = np.poly1d(z1)
# ax1.plot(diamArray, p1(diamArray))

# ax2.scatter(diams, noLamella, label='Number of Lamella')
# ax2.set_title('Number of lamella')
z2 = np.polyfit(diams[startIndexFit:], noLamella[startIndexFit:], 1)
p2 = np.poly1d(z2)
# ax2.plot(diamArray, p2(diamArray))

# ax3.scatter(diams, nodeDiam, label='Node and MYSA Diam')
# ax3.set_title('Node and MYSA Diameter')
z3 = np.polyfit(diams[startIndexFit:], nodeDiam[startIndexFit:], 2)
p3 = np.poly1d(z3)
# ax3.plot(diamArray, p3(diamArray))

# ax4.scatter(diams, FLUTLen, label='FLUT length')
# ax4.set_title('FLUT length')
z4 = np.polyfit(diams[startIndexFit:], FLUTLen[startIndexFit:], 1)
p4 = np.poly1d(z4)
# ax4.plot(diamArray, p4(diamArray))

# ax5.scatter(diams, STINLen, label='STIN length')
# ax5.set_title('STIN length')
z5 = np.polyfit(diams[startIndexFit:], STINLen[startIndexFit:], 1)
p5 = np.poly1d(z5)
# ax5.plot(diamArray, p5(diamArray))

# ax6.scatter(diams, FLUTDiam, label='FLUT and STIN diameter')
# ax6.set_title('FLUT and STIN diameter')
z6 = np.polyfit(diams[startIndexFit:], FLUTDiam[startIndexFit:], 2)
p6 = np.poly1d(z6)
# ax6.plot(diamArray, p6(diamArray))

# plt.legend()
# plt.show()

nodeVolume = pi*(np.array(nodeDiam)/2)**2 * nodeLen
noOfShannels = 2*pi*(np.array(nodeDiam)/2) * nodeLen * densityNaChannels

f, (ax1, ax2, ax3) = plt.subplots(3,1, sharex=True)

ax1.plot(diams, nodeVolume)
ax1.set_title('node volume')
ax2.plot(diams, noOfShannels)
ax2.set_title('# channels')
ax3.plot(diams, noOfShannels/nodeVolume)
ax3.set_title('# channels per node volume')

plt.show()
