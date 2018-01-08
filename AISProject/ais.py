#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import ais_parse as parse
from itertools import cycle
import pandas as pd
from matplotlib import colors as mcolors
from pandas import datetime as pdatetime
from sklearn.cluster import DBSCAN
from math import *


class ais:
    def __init__(self,input_path,segment):
        self.allcolors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
        self.colors = cycle(self.allcolors.values())
        self.by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
                        for name, color in self.allcolors.items())
        self.sorted_names = [name for hsv, name in self.by_hsv]
        self.data_paths = [os.path.join(input_path, s) for s in os.listdir(input_path)]
        self.tables = []
        self.seg_tab = []

        self.read_ais_data()
        if segment:
            self.segment_table_by_date()
        else:
            self.seg_tab = self.tables


    def compute_date(self,date0, date1):
        d1 = pdatetime.strptime(date0, '%Y-%m-%d %H:%M:%S')
        d2 = pdatetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
        return (d2 - d1).days

    def segment_table_by_date(self):
        for table in self.tables:
            # print table
            splite = [0]
            for idx in range(len(table) - 1):
                if self.compute_date(str(table.iloc[idx]['Date']), str(table.iloc[idx + 1]['Date'])) > 3:
                    splite.append(idx)
            splite.append(len(table))

            for idx in range(len(splite)-1):
                tmp = table[splite[idx]+1:splite[idx+1]-1]
                self.seg_tab.append(tmp)
        print "seg_tab length = %d"%len(self.seg_tab)

    def draw_segment_line(self):
        map = Basemap(projection='mill', lon_0=180, width=12000000, height=9000000)
        map.drawcoastlines()
        map.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0])
        map.drawmeridians(np.arange(map.lonmin, map.lonmax + 30, 60), labels=[0, 0, 0, 1])
        map.drawmapboundary(fill_color='white')
        map.drawcoastlines(linewidth=0.5, color='y')
        map.drawcountries(color='y')
        map.drawstates(color='y')
        map.fillcontinents(color='coral', lake_color='blue')

        for tmp in self.seg_tab:
            X = tmp['X'].values
            Y = tmp['Y'].values

            if X != [] and Y != []:
                lon, lat = map(X, Y)
                # fn = ('segment%d-%d.csv') % (shipMMSI, counter)
                # tmp.to_csv(fn)
                # counter += 1
                # current_label = ('%s %s %s t\n%s') % (shipMMSI, getNationFlag(shipMMSI), str(tmp['Dun'][0]),str(tmp['Date'][0]))
                current_label = ('%s') % (str(tmp['Dun'][0]))
                map.plot(lon, lat, c=self.sorted_names[np.random.randint(100, len(self.sorted_names))], linestyle='-',
                         marker='D',
                         markersize=1,
                         linewidth=2)
                plt.text(lon[0], lat[0], current_label)
                map.scatter(lon[0], lat[0], 60, c='green', marker='*', edgecolors='none', zorder=10)  # start
                map.scatter(lon[-1], lat[-1], 60, c='red', marker='*', edgecolors='none', zorder=10)  # end

        plt.title('AIS ShipLine')
        plt.show()

    def read_ais_data(self):

        for file, color in zip(self.data_paths, self.colors):
            one_MMSI = []
            st_MMSI = []
            parse.get_data_ST(file, st_MMSI)
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
                    x[i] = 360 + x[i]  # correct longtitude

            y = np.array(y_list)
            table = pd.DataFrame(columns=['Date', 'X', 'Y', 'Dun'])
            table['Date'] = date
            table['X'] = x
            table['Y'] = y
            table['Dun'] = np.array(Dun_list)

            table.set_index('Date', drop=False, append=False, inplace=True, verify_integrity=False)
            table = table.sort_index()
            self.tables.append(table)

class Clustering:

    def __init__(self,ais):
        self.ais = ais
        self.pds = ais.seg_tab
        self.Acenter_x = []
        self.Acenter_y = []

    def hausdorff(self,l1, l2):
        def euclidDist(p1, p2):
            dist = sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
            return dist

        X1s = l1['X'].values
        Y1s = l1['Y'].values
        X2s = l2['X'].values
        Y2s = l2['Y'].values
        points1 = [(X1s[idx], Y1s[idx]) for idx in range(len(X1s))]
        points2 = [(X2s[idx], Y2s[idx]) for idx in range(len(X2s))]
        # print len(points1)
        # print len(points2)
        distances = np.zeros(len(points1))
        for idx1 in range(len(points1)):
            currentdist = sys.maxint
            for idx2 in range(len(points2)):
                tmpdist = euclidDist(points1[idx1], points2[idx2])
                currentdist = min(currentdist, tmpdist)
            distances[idx1] = currentdist
        return max(distances)

    def createDistanceMatrix(self):
        rows, cols = len(self.pds), len(self.pds)
        self.distMat = np.zeros((rows, cols))

        # segment into servals lines
        for x in range(rows):
            for y in range(cols):
                if x == y:
                    continue
                self.distMat[x, y] = self.hausdorff(self.pds[x], self.pds[y])
                self.distMat[y, x] = self.hausdorff(self.pds[y], self.pds[x])

    def clusterAgglomerartive(self,cn=4):

        # Update a distance matrix and std deviations
        self.createDistanceMatrix()

        dunMap = [(self.pds[i]['Dun'].values)[0] for i in range(len(self.distMat[0]))]
        print dunMap
        self.clusters = [[i] for i in range(len(self.distMat[0]))]

        while len(self.clusters) > cn:
            affMat = np.zeros((len(self.clusters), len(self.clusters)))
            for r in range(affMat.shape[0] - 1):
                for c in range(r + 1, affMat.shape[1]):
                    ## count inter-cluster average distance
                    dist = 0

                    for t1idx in self.clusters[r]:
                        for t2idx in self.clusters[c]:
                            # distance of trajectory t1 (t1 in tA) and trajectory t2 (t2 in tB)
                            # dist += 1 / ((self.distMat[t1idx, t2idx] * self.distMat[t2idx, t1idx]) + 1e-6)
                            dist += (dunMap[t1idx]/10000.0 + dunMap[t2idx]/10000.0) / ((self.distMat[t1idx,
                                                                            t2idx] * self.distMat[t2idx,t1idx]) + 1e-6)

                    dist *= 1.0 / (len(self.clusters[r]) * len(self.clusters[c]))
                    affMat[r, c] = dist

            # Find two closest clusters and merge them
            # First trajectory is given by row index, second trajectory is given by column index of affinity matrix
            t1idx = np.argmax(affMat) / affMat.shape[1]
            t2idx = np.argmax(affMat) % affMat.shape[0]

            self.clusters[t1idx].extend(self.clusters[t2idx])
            self.clusters = [self.clusters[i] for i in range(len(self.clusters)) if i != t2idx]


        # Assign an estimated cluster index to each trajectory
        for i in range(len(self.clusters)):
            for j in self.clusters[i]:
                print('line %d belongs to %d') % (j, i)
        print self.clusters

    def _DBSCAN(self,X,Y):
        center_x = []
        center_y = []
        X = np.array(X).reshape(-1,1)
        Y = np.array(Y).reshape(-1,1)
        data = np.hstack((X, Y))

        model = DBSCAN(eps=150000, min_samples=15)
        model.fit(data)
        y_hat = model.labels_

        core_indices = np.zeros_like(y_hat, dtype=bool)
        core_indices[model.core_sample_indices_] = True

        y_unique = np.unique(y_hat)
        clrs = plt.cm.Spectral(np.linspace(0, 0.8, y_unique.size))
        # data[:, 0], data[:, 1] = map(data[:, 0], data[:, 1])
        for k, clr in zip(y_unique, clrs):
            cur = (y_hat == k)
            if k == -1:
                # map.scatter(data[cur,0],data[cur,1],s=1,c='black') # nosie
                continue
            # map.scatter(data[cur, 0], data[cur, 1], s=40, c=color,marker='*')

            center_x.extend(data[cur, 0])
            center_y.extend(data[cur, 1])

        self.Acenter_x.append(center_x)
        self.Acenter_y.append(center_y)

        # map.plot(center_x, center_y,c=sorted_names[np.random.randint(100,len(sorted_names))],linestyle='-',
        #              markersize=3,
        #              linewidth=1)

    def cluster_center(self):
        # tmp = [[0, 1, 3, 2], [4, 6], [5, 7], [8, 9, 10, 12, 11]]
        tmp = self.clusters
        print "pds=",len(self.pds)
        self.dun = [] # Dun Wei
        for ix in range(len(tmp)):
            AX = []
            AY = []
            clus = []
            for iy in range(len(tmp[ix])):
                tmppd = self.pds[tmp[ix][iy]]
                X = tmppd['X'].values
                Y = tmppd['Y'].values
                AX.extend(X)
                AY.extend(Y)
                clus.append((tmppd['Dun'].values)[0])
            self.dun.append(clus)
            self._DBSCAN(AX,AY)

        print len(self.Acenter_x),len(self.Acenter_x[0]),self.Acenter_x
        print len(self.Acenter_y),len(self.Acenter_y[0]),self.Acenter_y

    def draw_segment_line(self):
        map = Basemap(projection='mill', lon_0=180, width=12000000, height=9000000)
        map.drawcoastlines()
        map.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0])
        map.drawmeridians(np.arange(map.lonmin, map.lonmax + 30, 60), labels=[0, 0, 0, 1])
        map.drawmapboundary(fill_color='white')
        map.drawcoastlines(linewidth=0.5, color='y')
        map.drawcountries(color='y')
        map.drawstates(color='y')
        map.fillcontinents(color='coral', lake_color='blue')

        for ix in range(len(self.Acenter_x)):
            X = np.array(self.Acenter_x[ix])
            Y = np.array(self.Acenter_y[ix])
            current_label = ""
            for dunix in range(len(self.dun[ix])):
                current_label += (str(self.dun[ix][dunix]) + "t\n")

            if X != [] and Y != []:
                lon, lat = map(X, Y)

                map.scatter(lon,lat, s=40, c=self.ais.sorted_names[np.random.randint(100, len(self.ais.sorted_names))], marker='*')
                # map.plot(lon, lat, c=self.ais.sorted_names[np.random.randint(100, len(self.ais.sorted_names))],
                #          linestyle='--',
                #              marker='D',
                #              markersize=1,
                #              linewidth=2)
                plt.text(lon[0], lat[0], current_label)
                # map.scatter(lon[0], lat[0], 60, c='green', marker='*', edgecolors='none', zorder=10)  # start
                # map.scatter(lon[-1], lat[-1], 60, c='red', marker='*', edgecolors='none', zorder=10)  # end

        plt.title('AIS Clustering ShipLine')
        plt.show()

if __name__ == "__main__":

    a = ais('/media/xxxx/xx/AISProject/Show',False)
    # a.read_ais_data()
    # a.segment_table_by_date()
    a.draw_segment_line()
    cls = Clustering(a)
    cls.clusterAgglomerartive(14)
    cls.cluster_center()
    cls.draw_segment_line()