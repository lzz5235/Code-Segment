import os
import numpy as np
import sys as sys
import matplotlib as mpl
import matplotlib.colors
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import ais_parse as parse
from itertools import cycle
import pandas as pd
from matplotlib import colors as mcolors
from pandas import datetime as pdatetime
from ais_conv import getNationFlag
from sklearn.cluster import DBSCAN
from math import *
from scipy.cluster.vq import kmeans
from scipy.cluster.vq import kmeans2
import random
from scipy.spatial.distance import euclidean
from scipy import spatial

allcolors = dict(mcolors.BASE_COLORS,**mcolors.CSS4_COLORS)
by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])),name)
                for name,color in allcolors.items())

sorted_names = [name for hsv, name in by_hsv]
print sorted_names

def map_AllLine(DirectoryPath):

    def compute_date(date0, date1):
        d1 = pdatetime.strptime(date0, '%Y-%m-%d %H:%M:%S')
        d2 = pdatetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
        return (d2 - d1).days

    map = Basemap(projection='mill', lon_0=180, width=12000000, height=9000000)
    map.drawcoastlines()
    map.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0])
    map.drawmeridians(np.arange(map.lonmin, map.lonmax + 30, 60), labels=[0, 0, 0, 1])
    map.drawmapboundary(fill_color='white')
    map.drawcoastlines(linewidth=0.5, color='y')
    map.drawcountries(color='y')
    map.drawstates(color='y')
    map.fillcontinents(color='coral', lake_color='blue')
    colors = cycle(allcolors.values())
    data_paths = [os.path.join(DirectoryPath, s) for s in os.listdir(DirectoryPath)]
    counter = 1
    for file,color in zip(data_paths,colors):
        one_MMSI = []
        st_MMSI = []
        parse.get_data_ST(file,st_MMSI)
        shipdata = st_MMSI[0]
        shipMMSI = shipdata['MMSI']
        Length = int(shipdata['StaticInfo'][0]['Length'])
        Width = int(shipdata['StaticInfo'][0]['Width'])
        Draught = int(shipdata['StaticInfo'][0]['Draught'])
        Dun = Length * Width * Draught

        parse.get_data_DY(file, one_MMSI)
        x_list = []
        y_list = []
        date_list = []
        Dun_list = []
        for shipdata in one_MMSI:
            shipMMSI = shipdata['MMSI']
            x = shipdata['DynamicInfo'][0]['Longitude']  # jingdu
            y = shipdata['DynamicInfo'][0]['Latitude']  # weidu
            datetime = shipdata['DynamicInfo'][0]['LastTime']
            date_list.append(datetime)
            x_list.append(x)
            y_list.append(y)
            Dun_list.append(Dun)

        date = np.array(date_list)
        x = np.array(x_list)

        for i in range((x.shape)[0]):
            if x[i] <= 0:
                x[i] = 360 + x[i] # correct longtitude

        y = np.array(y_list)
        table = pd.DataFrame(columns=['Date', 'X', 'Y' , 'Dun'])
        table['Date'] = date
        table['X'] = x
        table['Y'] = y
        table['Dun'] = np.array(Dun_list)

        table.set_index('Date', drop=False, append=False, inplace=True, verify_integrity=False)
        table = table.sort_index()
        # table.to_csv('look.csv')
        # table = table.iloc[608:989]

        print table
        splite = [0]
        for idx in range(len(table)-1):
            if compute_date(str(table.iloc[idx]['Date']),str(table.iloc[idx+1]['Date'])) > 3:
                splite.append(idx)

        splite.append(len(table))

        for idx in range(len(splite)-1):
            tmp = table[splite[idx]+1:splite[idx+1]-1]
            X = tmp['X'].values
            Y = tmp['Y'].values

            if X !=[] and Y!=[]:
                lon, lat = map(X, Y)
                fn = ('segment%d-%d.csv') % (shipMMSI,counter)
                tmp.to_csv(fn)
                counter += 1
                current_label = ('%s %s %s t\n%s') % (shipMMSI,getNationFlag(shipMMSI),str(tmp['Dun'][0]),
                                                        str(tmp['Date'][0]))
                map.plot(lon, lat,c=sorted_names[np.random.randint(100,len(sorted_names))],linestyle='-',marker='D',
                         markersize=1,
                         linewidth=2)
                plt.text(lon[0], lat[0],current_label)
                map.scatter(lon[0], lat[0], 60, c='green', marker='*', edgecolors='none', zorder=10) # start
                map.scatter(lon[-1], lat[-1], 60,c='red',marker='*',edgecolors='none', zorder=10) # end

                # print X[0],Y[0],X[-1],Y[-1]


    plt.title('All ShipLine')
    plt.show()

def hausdorff(l1,l2):
    def euclidDist(p1, p2):
        dist = sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
        return dist

    X1s = l1['X'].values
    Y1s = l1['Y'].values
    X2s = l2['X'].values
    Y2s = l2['Y'].values
    points1 = [(X1s[idx],Y1s[idx]) for idx in range(len(X1s))]
    points2 = [(X2s[idx],Y2s[idx]) for idx in range(len(X2s))]
    # print len(points1)
    # print len(points2)
    distances = np.zeros(len(points1))
    for idx1 in range(len(points1)):
        currentdist = sys.maxint
        for idx2 in range(len(points2)):
            tmpdist = euclidDist(points1[idx1],points2[idx2])
            currentdist = min(currentdist,tmpdist)
        distances[idx1] = currentdist
    return max(distances)

def Inital_Points(pds):
    rows,cols = len(pds),len(pds)
    distMat = np.zeros((rows, cols))

    # segment into servals lines
    for x in range(rows):
        for y in range(cols):
            if x == y:
                continue
            distMat[x,y] = hausdorff(pds[x],pds[y])
            distMat[y,x] = hausdorff(pds[y],pds[x])
    return distMat

# def createDistanceMatrix():
#     size = len(self.trajectories)
#     self.distMat = np.ones((size, size))
#
#     for r in range(size):
#         for c in range(size):
#             dist = self.modHausDist(r, c)
#             self.distMat[r, c] *= dist

def clusterAgglomerartive(pds,cn):

    # Update a distance matrix and std deviations
    distMat = Inital_Points(pds)

    clusters = [[i] for i in range(len(distMat[0]))]

    while len(clusters) > cn:
        affMat = np.zeros((len(clusters), len(clusters)))
        for r in range(affMat.shape[0] - 1):
            for c in range(r + 1, affMat.shape[1]):
                ## count inter-cluster average distance
                dist = 0

                for t1idx in clusters[r]:
                    for t2idx in clusters[c]:
                        # distance of trajectory t1 (t1 in tA) and trajectory t2 (t2 in tB)
                        dist += 1 / ((distMat[t1idx, t2idx] * distMat[t2idx, t1idx]) + 1e-6)

                dist *= 1.0 / (len(clusters[r]) * len(clusters[c]))
                affMat[r, c] = dist

        # Find two closest clusters and merge them
        # First trajectory is given by row index, second trajectory is given by column index of affinity matrix
        t1idx = np.argmax(affMat) / affMat.shape[1]
        t2idx = np.argmax(affMat) % affMat.shape[0]

        clusters[t1idx].extend(clusters[t2idx])
        clusters = [clusters[i] for i in range(len(clusters)) if i != t2idx]

    # Assign an estimated cluster index to each trajectory
    for i in range(len(clusters)):
        for j in clusters[i]:
            print('line %d belongs to %d')%(j,i)
    print clusters

def clusterSpectral(pds,cn):
    stdNN = 2
    stdMin = 0.4
    stdMax = 20.0
    stdDevs = np.zeros((0, 0))
    def createStdDevs(distMat):
        rowSortedDistMat = np.copy(distMat)
        rowSortedDistMat.sort(axis = 1)

        stdDevs = rowSortedDistMat[:, min(stdNN, rowSortedDistMat.shape[1] - 1)]
        for i in range(len(stdDevs)):
            stdDevs[i] = max(stdMin, min(stdMax, stdDevs[i]))
        return stdDevs

    def std(tidx):
        return stdDevs[tidx]
    def similarity(distMat,t1idx, t2idx):
        return exp( -(distMat[t1idx, t2idx] * distMat[t2idx, t1idx]) / (2 * std(t1idx) * std(t2idx)) )
    # Update a distance matrix and std deviations

    distMat = Inital_Points(pds)
    stdDevs = createStdDevs(distMat)

    K = np.zeros((len(distMat[0]), len(distMat[0])))
    for r in range(len(distMat[0])):
        for c in range(len(distMat[0])):
            K[r, c] = similarity(distMat,r, c)

    # Diagonal matrix W for normalization
    W = np.diag(1.0 / np.sqrt(np.sum(K, 1)))

    # Normalized affinity matrix
    L = np.dot(np.dot(W, K), W)

    # Eigendecomposition
    Eval, Evec = np.linalg.eig(L)

    gMin, gMax = 0, 0
    for val in Eval:
        if val > 0.8:
            gMax += 1
            if val > 0.99:
                gMin += 1

    # Sort eigenvalues and eigenvectors according to descending eigenvalue
    Eval, Evec = zip(*sorted(zip(Eval, Evec.T), reverse=True))
    Evec = np.array(Evec).T

    g = -1
    if g == -1:
        ## Estimate the number of clusters
        # Distortion scores for different number of clusters g
        rhog = np.zeros(gMax - gMin + 1)

        for g in range(gMin, gMax + 1):
            V = np.copy(Evec[:, 0:g])
            S = np.diag(1.0 / np.sqrt(np.sum(np.multiply(V, V), 1)))
            R = np.dot(S, V)

            # k-means clustering of the row vectors of R
            cb, wcScatt = kmeans(R, g, iter=20, thresh=1e-05)  # cb = codebook (centroids = rows of cb)

            # compute distortion score rho_g (withit class scatter /  sum(within class scatter, total scatter))
            totScatt = np.sum([np.linalg.norm(r - c) for r in R for c in cb])
            rhog[g - gMin] = wcScatt / (totScatt - wcScatt)

        # Best number of centroids.
        g = gMin + np.argmin(rhog)

    print("Number of centroids = %d" % g)

    # Prerfofm classification of trajectories using k-means clustering
    V = np.copy(Evec[:, 0:g])
    S = np.diag(1.0 / np.sqrt(np.sum(np.multiply(V, V), 1)))
    R = np.dot(S, V)

    ## Find g initial centroids (rows)
    initCentroids = np.zeros((g, R.shape[1]))
    # Matrix of distance of each observation (rows) to each initial centroid (columns)
    initCentroidsDist = np.zeros((R.shape[0], g))

    initCentroids[0] = R[random.randint(0, R.shape[0] - 1)]
    for i in range(g - 1):
        # get each observation's distance to the new centroid
        initCentroidsDist[:, i] = [spatial.distance.euclidean(obs, initCentroids[i]) for obs in R]

        # get the observation which has the worst minimal distance to some already existing centroid
        newidx = np.argmax(np.min(initCentroidsDist[:, :(i + 1)], 1))
        initCentroids[i + 1] = R[newidx]

    controids, labels = kmeans2(R, initCentroids, iter=10, thresh=1e-05, minit='matrix', missing='warn')
    print controids,labels
    # assert (len(trajectories) == len(labels))
    #
    # for i in range(len(clusters)):
    #     for j in clusters[i]:
    #         print('line %d belongs to %d')%(j,i)

if __name__ == "__main__":
    all_MMSI = []
    one_MMSI = []
    all_MMSI_DY = []
    pds = []

    # map_AllLine('/media/iscas/1FE010E3268C15CA/AISProject/Show') # All shipline
    # Inital_Points('segment432759000-1.csv', 'segment432759000-2.csv')
    data_paths = [os.path.join("./segment/", s) for s in os.listdir('./segment/')]
    for file in data_paths:
        pds.append(pd.read_csv(file))
        print file
    clusterAgglomerartive(pds,4)
    # clusterSpectral(pds,2)
