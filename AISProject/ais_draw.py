#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import numpy as np
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

allcolors = dict(mcolors.BASE_COLORS,**mcolors.CSS4_COLORS)
by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])),name)
                for name,color in allcolors.items())

sorted_names = [name for hsv, name in by_hsv]
print sorted_names

def mapscatter(all_MMSI):
    x_list = []
    y_list = []
    for shipdata in all_MMSI:
        x = shipdata['DynamicInfo'][0]['Longitude'] #jingdu
        y = shipdata['DynamicInfo'][0]['Latitude']  #weidu

        if x <=0:
            x = 360 + x

        x_list.append(x)
        y_list.append(y)
    x = np.array(x_list)
    y = np.array(y_list)
    map = Basemap(projection='mill', lon_0=180, width=12000000, height=9000000)
    map.drawcoastlines()
    map.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0])
    map.drawmeridians(np.arange(map.lonmin, map.lonmax + 30, 60), labels=[0, 0, 0, 1])
    map.drawmapboundary(fill_color='white')
    map.drawcoastlines(linewidth=0.5, color='y')
    map.drawcountries(color='y')
    map.drawstates(color='y')
    map.fillcontinents(color='coral', lake_color='blue')
    x, y = map(x, y)
    map.scatter(x,y,25,cmap=plt.cm.jet,marker='o',edgecolors='none',zorder=10)
    plt.title('Ship Map')
    plt.show()

def mapscatter(*all_MMSI): # cargo/tanker
    labels = [u'货船',u'油轮']
    mpl.rcParams['font.sans-serif'] = [u'SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
    map = Basemap(projection='mill', lon_0=180, width=12000000, height=9000000)
    map.drawcoastlines()
    map.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0])
    map.drawmeridians(np.arange(map.lonmin, map.lonmax + 30, 60), labels=[0, 0, 0, 1])
    map.drawmapboundary(fill_color='white')
    map.drawcoastlines(linewidth=0.5, color='y')
    map.drawcountries(color='y')
    map.drawstates(color='y')
    map.fillcontinents(color='coral', lake_color='blue')
    for idx,lst in enumerate(all_MMSI):
        x_list = []
        y_list = []
        for shipdata in lst:
            x = shipdata['DynamicInfo'][0]['Longitude'] #jingdu
            y = shipdata['DynamicInfo'][0]['Latitude']  #weidu

            if x <=0:
                x = 360 + x

            x_list.append(x)
            y_list.append(y)
        x = np.array(x_list)
        y = np.array(y_list)
        x, y = map(x, y)
        map.scatter(x,y,5,cmap=plt.cm.jet,marker='o',label=labels[idx])
    plt.legend(loc='lower left')
    plt.title(u'货船与油轮的轨迹')
    plt.show()

def mapline(one_MMSI):
    x_list = []
    y_list = []
    date_list = []
    isTagret = False

    for shipdata in one_MMSI:
        shipMMSI = shipdata['MMSI']
        x = shipdata['DynamicInfo'][0]['Longitude']  # jingdu
        y = shipdata['DynamicInfo'][0]['Latitude']  # weidu
        datetime = shipdata['DynamicInfo'][0]['LastTime']

        date_list.append(datetime)
        x_list.append(x)
        y_list.append(y)

    date = np.array(date_list)
    x = np.array(x_list)
    rows = x.shape
    for i in range(rows[0]):
        if x[i] <=0:
            x[i] = 360 + x[i]

    y = np.array(y_list)
    table = pd.DataFrame(columns=['Date','X','Y'])
    table['Date'] = date
    table['X'] = x
    table['Y'] = y

    table.set_index('Date',drop=True,append=False,inplace=True,verify_integrity=False)
    table = table.sort_index()
    # print table
    # np.set_printoptions(edgeitems=100)
    # print np.array(table['X'])
    # print np.array(table['Y'])

    map = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,llcrnrlon=0,urcrnrlon=360,resolution='c')
    map.drawcoastlines()
    map.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0])
    map.drawmeridians(np.arange(map.lonmin, map.lonmax + 30, 60), labels=[0, 0, 0, 1])
    # fill continents 'coral' (with zorder=0), color wet areas 'aqua'
    map.drawmapboundary(fill_color='white')
    print table['X'],table['Y']
    x, y = map(np.array(table['X']), np.array(table['Y']))
    map.plot(x[1:-1], y[1:-1],'o-')
    map.scatter(x[0], y[0], 60, c='green', marker='*', edgecolors='none', zorder=10)  # start
    map.scatter(x[-1], y[-1], 60, c='red', marker='*', edgecolors='none', zorder=10)  # end

    map.drawcoastlines(linewidth=0.5, color='y')
    map.drawcountries(color='y')
    map.drawstates(color='y')
    map.fillcontinents(color='grey', lake_color='black')
    plt.title('%s ShipLine' %shipMMSI)
    plt.show()
    plt.cla()
    return isTagret,table

def mapline_from_tables():
    map = Basemap(projection='merc', llcrnrlat=25, llcrnrlon=115, urcrnrlat=60, urcrnrlon=160,
                  resolution='c', width=12000000, height=9000000)
    map.drawcoastlines()
    map.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0])
    map.drawmeridians(np.arange(map.lonmin, map.lonmax + 30, 60), labels=[0, 0, 0, 1])
    # fill continents 'coral' (with zorder=0), color wet areas 'aqua'
    map.drawmapboundary(fill_color='white')

    data_paths = [os.path.join("./CHU_Japan_test/", s) for s in os.listdir('./CHU_Japan_test/')]
    for file in data_paths:
        data = parse.read_data_DY_TXT(file)

        # print np.array(data.iloc[:,1].values),np.array(data.iloc[:,0].values)
        x, y = map(data.iloc[:,1].values, data.iloc[:,0].values)
        # print x,y
        # map.plot(x, y,'o-')
        map.plot(x, y, c=sorted_names[np.random.randint(100, len(sorted_names))], linestyle='-', marker='D',
             markersize=1,
             linewidth=2)

    map.drawcoastlines(linewidth=0.5, color='y')
    map.drawcountries(color='y')
    map.drawstates(color='y')
    map.fillcontinents(color='grey', lake_color='black')
    plt.title('2013.11 Japanese ShipLine')
    plt.show()
    plt.cla()

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

def map_AllPoint(DirectoryPath):
    def _DBSCAN(X,Y,color):
        center_x = []
        center_y = []
        X = X.reshape(-1,1)
        Y = Y.reshape(-1,1)
        data = np.hstack((X, Y))

        model = DBSCAN(eps=0.015, min_samples=2)
        model.fit(data)
        y_hat = model.labels_

        core_indices = np.zeros_like(y_hat, dtype=bool)
        core_indices[model.core_sample_indices_] = True

        y_unique = np.unique(y_hat)
        clrs = plt.cm.Spectral(np.linspace(0, 0.8, y_unique.size))
        data[:, 0], data[:, 1] = map(data[:, 0], data[:, 1])
        for k, clr in zip(y_unique, clrs):
            cur = (y_hat == k)
            if k == -1:
                map.scatter(data[cur,0],data[cur,1],s=1,c='black') # nosie
                continue
            map.scatter(data[cur, 0], data[cur, 1], s=40, c=color,marker='*')

            center_x.extend(data[cur, 0])
            center_y.extend(data[cur, 1])

        map.plot(center_x, center_y,c=sorted_names[np.random.randint(100,len(sorted_names))],linestyle='-',
                     markersize=3,
                     linewidth=1)

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

    for file,color in zip(data_paths,colors):
        table = pd.DataFrame(columns=['Date', 'X', 'Y', 'Course'])
        X = []
        Y = []
        one_MMSI = []
        parse.get_data_DY(file, one_MMSI)
        x_list = []
        y_list = []
        date_list = []
        course_list = []
        speed_list = []
        for shipdata in one_MMSI:
            shipMMSI = shipdata['MMSI']
            x = shipdata['DynamicInfo'][0]['Longitude']  # jingdu
            y = shipdata['DynamicInfo'][0]['Latitude']  # weidu
            datetime = shipdata['DynamicInfo'][0]['LastTime']
            course = shipdata['DynamicInfo'][0]['course']
            speed = shipdata['DynamicInfo'][0]['Speed']
            date_list.append(datetime)
            course_list.append(course)
            speed_list.append(speed)
            x_list.append(x)
            y_list.append(y)

        date = np.array(date_list)
        x = np.array(x_list)

        for i in range((x.shape)[0]):
            if x[i] <= 0:
                x[i] = 360 + x[i] # correct longtitude

        y = np.array(y_list)

        tab = pd.DataFrame(columns=['Date', 'X', 'Y', 'Course', 'Speed'])
        tab['Date'] = date
        tab['X'] = x
        tab['Y'] = y
        tab['Course'] = np.array(course_list)
        tab['Speed'] = np.array(speed_list)
        table = pd.concat([table,tab])

        table.set_index('Date', drop=False, append=False, inplace=True, verify_integrity=False)
        table = table.sort_index()
        print table
        # table.to_csv('look.csv')
        west_east_splite = []
        if table.iloc[0]['Course'] > 180:
            west_east_splite.append(0)
        else:
            west_east_splite.append(0)

        for idx in range(len(table) - 1):
            if float(table.iloc[idx]['Course']) > 180 and float(table.iloc[idx+1]['Course']) < 180:
                west_east_splite.append(idx)
            # elif float(table.iloc[idx]['Course']) < 180 and float(table.iloc[idx+1]['Course']) > 180:
            #     west2east.append(idx)

        west_east_splite.append(len(table) - 1)


        X = table['X'].values
        Y = table['Y'].values

        if X !=[] and Y!=[]:
            _DBSCAN(X,Y,color)
            lon, lat = map(X, Y)
            # map.scatter(lon, lat,c='b',marker='D',s=1)

    plt.title('Japan ShipLine')
    plt.show()

if __name__ == "__main__":
    all_MMSI = []
    one_MMSI = []
    all_MMSI_DY = []

    path = "/media/xxxx/xx/AISProject/Hawaii/tanker"
    data_paths = [os.path.join(path, s) for s in os.listdir(path)]
    for file in data_paths:
        one_MMSI = []
        parse.get_data_DY(file, one_MMSI)
        mapline(one_MMSI)

